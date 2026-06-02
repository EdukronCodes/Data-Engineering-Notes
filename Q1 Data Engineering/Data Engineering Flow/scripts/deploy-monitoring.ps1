param(
  [string]$ProvisionedPath = (Join-Path $PSScriptRoot "..\infra\provisioned.dev.json"),
  [string]$ResourceGroupName,
  [string]$Location = "eastus",
  [string]$WorkspaceName,
  [switch]$DryRun
)
$ErrorActionPreference = "Stop"
function Invoke-AzQuiet([scriptblock]$Block) {
  $prev = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try { & $Block } finally { $ErrorActionPreference = $prev }
}

if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
  throw "Azure CLI (az) required. Install: https://aka.ms/installazurecliwindows"
}

$p = Get-Content $ProvisionedPath -Raw | ConvertFrom-Json
if (-not $ResourceGroupName) { $ResourceGroupName = $p.resourceGroup }
$suffix = if ($p.suffix) { $p.suffix } else { "3546" }
if (-not $WorkspaceName) { $WorkspaceName = "log-retailde-$suffix" }

Write-Host "=== Retail pipeline monitoring deployment ===" -ForegroundColor Cyan
Write-Host "Resource group: $ResourceGroupName"
Write-Host "Log Analytics:  $WorkspaceName"

if ($DryRun) {
  Write-Host "[DryRun] Would create Log Analytics, diagnostics, alerts, workbook"
  exit 0
}

# Log Analytics workspace
$lawExists = Invoke-AzQuiet { az monitor log-analytics workspace show -g $ResourceGroupName -n $WorkspaceName 2>$null }
if (-not $lawExists) {
  Write-Host "Creating Log Analytics workspace $WorkspaceName..."
  az monitor log-analytics workspace create -g $ResourceGroupName -n $WorkspaceName -l $Location --sku PerGB2018 -o none
} else {
  Write-Host "Log Analytics workspace already exists."
}

$lawId = az monitor log-analytics workspace show -g $ResourceGroupName -n $WorkspaceName --query id -o tsv
$lawCustomerId = az monitor log-analytics workspace show -g $ResourceGroupName -n $WorkspaceName --query customerId -o tsv

function Enable-Diagnostics {
  param([string]$ResourceId, [string]$Name, [string[]]$Logs, [string[]]$Metrics)
  $exists = Invoke-AzQuiet { az monitor diagnostic-settings list --resource $ResourceId --query "[?name=='$Name'].name" -o tsv 2>$null }
  if ($exists) {
    Write-Host "  Diagnostics '$Name' already enabled on $ResourceId"
    return
  }
  $logJson = ($Logs | ForEach-Object { @{ category = $_; enabled = $true } }) | ConvertTo-Json -Compress
  $metricJson = ($Metrics | ForEach-Object { @{ category = $_; enabled = $true } }) | ConvertTo-Json -Compress
  Write-Host "  Enabling diagnostics '$Name'..."
  Invoke-AzQuiet {
    az monitor diagnostic-settings create --name $Name --resource $ResourceId --workspace $lawId `
      --logs $logJson --metrics $metricJson -o none 2>$null
  }
}

# ADF diagnostics
$adfId = az datafactory show -g $ResourceGroupName -n $p.dataFactoryName --query id -o tsv
Enable-Diagnostics -ResourceId $adfId -Name "diag-adf-retail" `
  -Logs @("PipelineRuns","ActivityRuns","TriggerRuns") `
  -Metrics @("AllMetrics")

# Storage accounts
foreach ($st in @($p.storageLakeAccount, $p.storageSourcesAccount)) {
  $stId = az storage account show -g $ResourceGroupName -n $st --query id -o tsv
  Enable-Diagnostics -ResourceId $stId -Name "diag-$st" `
    -Logs @("StorageRead","StorageWrite","StorageDelete") `
    -Metrics @("Transaction","Ingress","Egress","SuccessE2ELatency")
}

# SQL Server
$sqlId = az sql server show -g $ResourceGroupName -n $p.sqlServer --query id -o tsv 2>$null
if ($sqlId) {
  Enable-Diagnostics -ResourceId $sqlId -Name "diag-sql-retail" `
    -Logs @("SQLSecurityAuditEvents","DevOpsOperationsAudit") `
    -Metrics @("AllMetrics")
  $dbId = az sql db show -g $ResourceGroupName -s $p.sqlServer -n $p.sqlDatabase --query id -o tsv 2>$null
  if ($dbId) {
    Enable-Diagnostics -ResourceId $dbId -Name "diag-sqldb-pos" `
      -Logs @("SQLInsights","QueryStoreRuntimeStatistics","Errors","DatabaseWaitStatistics") `
      -Metrics @("Basic","InstanceAndAppAdvanced","WorkloadManagement")
  }
}

# PostgreSQL
$pgId = az postgres flexible-server show -g $ResourceGroupName -n $p.postgresServer --query id -o tsv 2>$null
if ($pgId) {
  Enable-Diagnostics -ResourceId $pgId -Name "diag-postgres-retail" `
    -Logs @("PostgreSQLLogs","PostgreSQLFlexSessions","PostgreSQLFlexQueryStoreRuntime") `
    -Metrics @("AllMetrics")
}

# Cosmos DB
$cosmosId = az cosmosdb show -g $ResourceGroupName -n $p.cosmosAccount --query id -o tsv 2>$null
if ($cosmosId) {
  Enable-Diagnostics -ResourceId $cosmosId -Name "diag-cosmos-retail" `
    -Logs @("DataPlaneRequests","QueryRuntimeStatistics","PartitionKeyStatistics") `
    -Metrics @("Requests","SLI","MetadataRequests")
}

# Databricks workspace
$dbwId = az databricks workspace show -g $ResourceGroupName -n $p.databricksWorkspaceName --query id -o tsv 2>$null
if ($dbwId) {
  Enable-Diagnostics -ResourceId $dbwId -Name "diag-databricks-retail" `
    -Logs @("dbfs","clusters","accounts","jobs","notebook","workspace") `
    -Metrics @("AllMetrics")
}

# Key Vault
$kvId = az keyvault show -g $ResourceGroupName -n $p.keyVaultName --query id -o tsv 2>$null
if ($kvId) {
  Enable-Diagnostics -ResourceId $kvId -Name "diag-kv-retail" `
    -Logs @("AuditEvent") `
    -Metrics @("AllMetrics")
}

# Action group for alerts
$actionGroupName = "ag-retailde-ops-$suffix"
$agExists = Invoke-AzQuiet { az monitor action-group show -g $ResourceGroupName -n $actionGroupName 2>$null }
if (-not $agExists) {
  Write-Host "Creating action group $actionGroupName..."
  Invoke-AzQuiet { az monitor action-group create -g $ResourceGroupName -n $actionGroupName --short-name RetailDE -o none }
  $agExists = $true
}

# Deploy alerts via ARM (scheduled-query CLI extension is unreliable on Windows)
$alertTemplate = Join-Path $PSScriptRoot "..\infra\monitoring\alert-rules.json"
if ((Test-Path $alertTemplate) -and $agExists) {
  $agId = az monitor action-group show -g $ResourceGroupName -n $actionGroupName --query id -o tsv
  Write-Host "Deploying alert rules via ARM..."
  Invoke-AzQuiet {
    az deployment group create -g $ResourceGroupName -n "deploy-retail-alerts-$suffix" `
      --template-file $alertTemplate `
      --parameters logAnalyticsWorkspaceId=$lawId actionGroupId=$agId suffix=$suffix -o none 2>&1 | Write-Host
  }
}

# Deploy workbook
$workbookSource = Join-Path $PSScriptRoot "..\monitoring\workbook-retail-pipeline.json"
if (Test-Path $workbookSource) {
  Write-Host "Deploying Azure Monitor workbook..."
  $wbName = "workbook-retail-pipeline-$suffix"
  $serialized = Get-Content $workbookSource -Raw
  $wbPropsPath = Join-Path $env:TEMP "workbook-props.json"
  @{
    displayName = "Retail Data Pipeline Dashboard"
    serializedData = $serialized
    sourceId = $lawId
    category = "workbook"
  } | ConvertTo-Json -Depth 3 | Set-Content $wbPropsPath -Encoding utf8
  $wbExists = Invoke-AzQuiet { az resource show -g $ResourceGroupName -n $wbName --resource-type "microsoft.insights/workbooks" 2>$null }
  if ($wbExists) {
    Invoke-AzQuiet { az resource update -g $ResourceGroupName -n $wbName --resource-type "microsoft.insights/workbooks" --set properties=@$wbPropsPath -o none 2>&1 | Write-Host }
  } else {
    Invoke-AzQuiet { az resource create -g $ResourceGroupName -n $wbName --resource-type "microsoft.insights/workbooks" --location $Location --properties "@$wbPropsPath" -o none 2>&1 | Write-Host }
  }
}

# Update provisioned.dev.json
$monitoring = [ordered]@{
  logAnalyticsWorkspace = $WorkspaceName
  logAnalyticsWorkspaceId = $lawId
  logAnalyticsCustomerId = $lawCustomerId
  actionGroup = $actionGroupName
  alerts = @("alert-adf-pipeline-failure-$suffix")
  workbookName = "workbook-retail-pipeline-$suffix"
  deployedAt = (Get-Date).ToString("o")
}
$p | Add-Member -NotePropertyName monitoring -NotePropertyValue $monitoring -Force
$p | ConvertTo-Json -Depth 8 | Set-Content $ProvisionedPath -Encoding UTF8

Write-Host ""
Write-Host "Monitoring deployment complete." -ForegroundColor Green
Write-Host "Log Analytics: $WorkspaceName (customerId: $lawCustomerId)"
Write-Host "Workbook: Azure Portal > Monitor > Workbooks > Retail Data Pipeline Dashboard"
Write-Host "  Or: Resource group $ResourceGroupName > workbook-retail-pipeline-$suffix"
