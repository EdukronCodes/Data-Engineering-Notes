param(
  [string]$ProvisionedPath = (Join-Path $PSScriptRoot "..\infra\provisioned.dev.json"),
  [string]$DatabricksToken = $env:DATABRICKS_TOKEN,
  [switch]$SkipDatabricks,
  [switch]$Wait,
  [int]$PollSeconds = 30,
  [int]$MaxWaitMinutes = 120
)
$ErrorActionPreference = "Stop"

function Get-OrCreate-DatabricksCluster {
  param([string]$DatabricksHost, [string]$Token, [string]$ExistingId)
  if ($ExistingId -and $ExistingId -notmatch 'x{4,}') {
    Write-Host "Using configured cluster: $ExistingId"
    return $ExistingId
  }
  if (-not $Token) {
    Write-Warning @"
DATABRICKS_TOKEN not set — medallion bronze/silver/gold will fail.
Create cluster manually at $($p.databricksWorkspaceUrl):
  1. Compute > Create cluster (Single Node, Runtime 13.3 LTS)
  2. Copy cluster ID into infra/provisioned.dev.json -> databricksClusterId
  3. Upload notebooks from databricks/notebooks to workspace
Or: `$env:DATABRICKS_TOKEN = '<pat>' ; .\scripts\run-adf-master.ps1
"@
    return $ExistingId
  }
  $headers = @{ Authorization = "Bearer $Token"; "Content-Type" = "application/json" }
  $list = Invoke-RestMethod -Uri "https://$DatabricksHost/api/2.0/clusters/list" -Headers $headers -Method Get
  $running = $list.clusters | Where-Object { $_.state -in @("RUNNING", "PENDING", "RESTARTING") } | Select-Object -First 1
  if ($running) {
    Write-Host "Found existing cluster: $($running.cluster_id) ($($running.state))"
    return $running.cluster_id
  }
  Write-Host "Creating single-node Databricks cluster for retail medallion..."
  $body = @{
    cluster_name = "retail-medallion-adf"
    spark_version = "13.3.x-scala2.12"
    node_type_id = "Standard_DS3_v2"
    num_workers = 0
    autotermination_minutes = 60
    spark_conf = @{ "spark.databricks.cluster.profile" = "singleNode"; "spark.master" = "local[*]" }
    custom_tags = @{ project = "retail-data-pipeline"; purpose = "medallion" }
  } | ConvertTo-Json
  $created = Invoke-RestMethod -Uri "https://$DatabricksHost/api/2.0/clusters/create" -Headers $headers -Method Post -Body $body
  $clusterId = $created.cluster_id
  Write-Host "Cluster created: $clusterId — waiting for RUNNING..."
  $deadline = (Get-Date).AddMinutes(15)
  do {
    Start-Sleep -Seconds 15
    $info = Invoke-RestMethod -Uri "https://$DatabricksHost/api/2.0/clusters/get?cluster_id=$clusterId" -Headers $headers -Method Get
    Write-Host "  State: $($info.state)"
  } while ($info.state -notin @("RUNNING") -and (Get-Date) -lt $deadline)
  if ($info.state -ne "RUNNING") { throw "Cluster did not reach RUNNING state" }
  return $clusterId
}

$p = Get-Content $ProvisionedPath -Raw | ConvertFrom-Json
$dbwUrl = if ($p.databricksWorkspaceUrl -match '^https?://') { $p.databricksWorkspaceUrl.TrimEnd('/') } else { "https://$($p.databricksWorkspaceUrl.TrimEnd('/'))" }
$dbwHost = ($dbwUrl -replace '^https://','')

if (-not $SkipDatabricks) {
  $clusterId = Get-OrCreate-DatabricksCluster -DatabricksHost $dbwHost -Token $DatabricksToken -ExistingId $p.databricksClusterId
  if ($clusterId -and $clusterId -ne $p.databricksClusterId) {
    $p.databricksClusterId = $clusterId
    $p | ConvertTo-Json -Depth 8 | Set-Content $ProvisionedPath -Encoding UTF8
    Write-Host "Updated provisioned.dev.json with clusterId=$clusterId"
    & (Join-Path $PSScriptRoot "deploy-adf-artifacts.ps1") -ProvisionedPath $ProvisionedPath
  }
}

$params = [ordered]@{
  environment = "dev"
  storageAccountName = $p.storageLakeAccount
  sourceStorageAccountName = $p.storageSourcesAccount
  sourceStorageAccountUrl = $p.sourceStorageAccountUrl
  sourceContainer = $p.sourcesContainer
  lakeStorageAccountUrl = $p.lakeStorageAccountUrl
  lakeContainer = $p.lakeContainer
  landingPathPrefix = "landing"
  databricksWorkspaceUrl = $dbwUrl
  databricksClusterId = $p.databricksClusterId
  restCustomersBaseUrl = $(if ($p.restCustomersBaseUrl) { $p.restCustomersBaseUrl } else { "https://$($p.storageSourcesAccount).blob.core.windows.net/$($p.sourcesContainer)" })
  restCustomersPath = $(if ($p.restCustomersPath) { $p.restCustomersPath } else { "/customers/customers.json" })
}
$path = Join-Path $env:TEMP "adf-master-params.json"
($params | ConvertTo-Json) | Set-Content $path -Encoding utf8

Write-Host "Starting master pipeline on $($p.dataFactoryName)..."
$runId = az datafactory pipeline create-run -g $p.resourceGroup --factory-name $p.dataFactoryName --name pl_master_retail_pipeline --parameters "@$path" --query runId -o tsv
Write-Host "RunId: $runId"
Write-Host "Monitor: https://portal.azure.com/#view/Microsoft_Azure_DataFactory/DataFactoryBlade/activityRun/id/$($p.dataFactoryName)/runId/$runId"

if ($Wait) {
  Write-Host "Polling pipeline status (max $MaxWaitMinutes min)..."
  $deadline = (Get-Date).AddMinutes($MaxWaitMinutes)
  do {
    Start-Sleep -Seconds $PollSeconds
    $status = az datafactory pipeline-run show -g $p.resourceGroup --factory-name $p.dataFactoryName --run-id $runId --query status -o tsv
    Write-Host "  Status: $status ($(Get-Date -Format HH:mm:ss))"
  } while ($status -in @("Queued", "InProgress") -and (Get-Date) -lt $deadline)
  Write-Host "Final status: $status"
  if ($status -eq "Failed") {
    az datafactory activity-run query-by-pipeline-run -g $p.resourceGroup --factory-name $p.dataFactoryName --run-id $runId --last-updated-after (Get-Date).AddDays(-1).ToString("o") --last-updated-before (Get-Date).AddDays(1).ToString("o") -o table
    exit 1
  }
}

