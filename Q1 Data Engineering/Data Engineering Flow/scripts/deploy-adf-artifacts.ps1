param(
  [string]$ProvisionedPath = (Join-Path $PSScriptRoot "..\infra\provisioned.dev.json"),
  [string]$ResourceGroupName,
  [string]$DataFactoryName
)
$ErrorActionPreference = "Stop"
$p = Get-Content $ProvisionedPath -Raw | ConvertFrom-Json
if (-not $ResourceGroupName) { $ResourceGroupName = $p.resourceGroup }
if (-not $DataFactoryName) { $DataFactoryName = $p.dataFactoryName }
$adfRoot = Join-Path $PSScriptRoot "..\adf"
$dbwUrl = $p.databricksWorkspaceUrl
if (-not $dbwUrl) {
  $dbwHost = az databricks workspace show -g $ResourceGroupName -n $p.databricksWorkspaceName --query workspaceUrl -o tsv
  $dbwUrl = "https://$dbwHost"
}
if ($dbwUrl -notmatch '^https?://') { $dbwUrl = "https://$($dbwUrl.TrimEnd('/'))" }
$dbwDomain = ($dbwUrl -replace '^https://','')
$dbwResourceId = if ($p.databricksWorkspaceResourceId) {
  $p.databricksWorkspaceResourceId
} else {
  az databricks workspace show -g $ResourceGroupName -n $p.databricksWorkspaceName --query id -o tsv 2>$null
}
function Get-KvSecret([string]$Name) {
  if (-not $p.keyVaultName) { return $null }
  az keyvault secret show --vault-name $p.keyVaultName --name $Name --query value -o tsv 2>$null
}
function Invoke-AzQuiet([scriptblock]$Block) {
  $prev = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try { & $Block } finally { $ErrorActionPreference = $prev }
}
function Strip-ConnectVia($props) {
  if ($props.PSObject.Properties.Name -contains 'connectVia') {
    $props.PSObject.Properties.Remove('connectVia')
  }
  return $props
}
$lsMap = @{
  "ls_adls_retail_lake.json" = @{ storageAccountUrl = $p.lakeStorageAccountUrl }
  "ls_adls_retail_sources.json" = @{ storageAccountUrl = $p.sourceStorageAccountUrl }
  "ls_key_vault_retail.json" = @{ keyVaultUrl = $p.keyVaultUrl }
  "ls_azure_sql_pos.json" = @{ serverName = $p.sqlServer; databaseName = $p.sqlDatabase; userName = $p.sqlAdminUser }
  "ls_postgresql_inventory.json" = @{ serverName = "$($p.postgresServer).postgres.database.azure.com"; databaseName = $p.postgresDatabase; userName = $p.postgresAdminUser }
  "ls_cosmos_stores.json" = @{ accountEndpoint = "https://$($p.cosmosAccount).documents.azure.com:443/"; databaseName = $p.cosmosDatabase }
  "ls_rest_customers.json" = @{ baseUrl = $(if ($p.restCustomersBaseUrl) { $p.restCustomersBaseUrl } else { "https://$($p.storageSourcesAccount).blob.core.windows.net/$($p.sourcesContainer)" }) }
  "ls_databricks_retail.json" = @{
    workspaceUrl = $dbwDomain
    workspaceResourceId = $dbwResourceId
    clusterId = $p.databricksClusterId
  }
}
$order = @('ls_key_vault_retail.json','ls_adls_retail_lake.json','ls_adls_retail_sources.json','ls_azure_sql_pos.json','ls_postgresql_inventory.json','ls_cosmos_stores.json','ls_rest_customers.json','ls_databricks_retail.json')
foreach ($fileName in $order) {
  $f = Join-Path $adfRoot "linkedService\$fileName"
  if (-not (Test-Path $f)) { continue }
  $raw = Get-Content $f -Raw | ConvertFrom-Json
  if ($lsMap.ContainsKey($fileName)) {
    foreach ($k in $lsMap[$fileName].Keys) {
      if ($raw.properties.parameters.PSObject.Properties.Name -contains $k) {
        $raw.properties.parameters.$k.defaultValue = $lsMap[$fileName][$k]
      }
    }
  }
  if ($fileName -eq 'ls_databricks_retail.json') {
    foreach ($k in $lsMap[$fileName].Keys) {
      if ($raw.properties.parameters.PSObject.Properties.Name -contains $k) {
        if ($k -eq 'workspaceUrl') {
          $raw.properties.parameters.$k.defaultValue = "https://$($lsMap[$fileName][$k] -replace '^https://','')"
        } else {
          $raw.properties.parameters.$k.defaultValue = $lsMap[$fileName][$k]
        }
      }
    }
    $raw.properties.typeProperties.PSObject.Properties.Remove('encryptedCredential')
  }
  if ($fileName -eq 'ls_postgresql_inventory.json') {
    $pgPwd = Get-KvSecret 'postgres-admin-password'
    if ($pgPwd) {
      Invoke-AzQuiet { az datafactory linked-service delete -g $ResourceGroupName --factory-name $DataFactoryName --name $raw.name -y -o none 2>$null }
      $raw.properties.typeProperties.password = @{ type = 'SecureString'; value = $pgPwd }
      $raw.properties.typeProperties.PSObject.Properties.Remove('authenticationType')
      $raw.properties.typeProperties | Add-Member -NotePropertyName authenticationType -NotePropertyValue 'Basic' -Force
    }
  }
  $props = Strip-ConnectVia $raw.properties
  $propsPath = Join-Path $env:TEMP "adf-ls-$($raw.name).json"
  $props | ConvertTo-Json -Depth 100 | Set-Content $propsPath -Encoding utf8
  Write-Host "LinkedService $($raw.name)"
  az datafactory linked-service create -g $ResourceGroupName --factory-name $DataFactoryName --name $raw.name --properties "@$propsPath" -o none
}
foreach ($f in Get-ChildItem (Join-Path $adfRoot "dataset") -Filter *.json) {
  $raw = Get-Content $f.FullName -Raw | ConvertFrom-Json
  $propsPath = Join-Path $env:TEMP "adf-ds-$($raw.name).json"
  $raw.properties | ConvertTo-Json -Depth 100 | Set-Content $propsPath -Encoding utf8
  Write-Host "Dataset $($raw.name)"
  az datafactory dataset create -g $ResourceGroupName --factory-name $DataFactoryName --name $raw.name --properties "@$propsPath" -o none
}
foreach ($f in Get-ChildItem (Join-Path $adfRoot "pipeline") -Filter *.json) {
  $raw = Get-Content $f.FullName -Raw | ConvertFrom-Json
  $pipePath = Join-Path $env:TEMP "adf-pl-$($raw.name).json"
  $raw.properties | ConvertTo-Json -Depth 100 | Set-Content $pipePath -Encoding utf8
  Write-Host "Pipeline $($raw.name)"
  az datafactory pipeline create -g $ResourceGroupName --factory-name $DataFactoryName --name $raw.name --pipeline "@$pipePath" -o none
}
foreach ($f in Get-ChildItem (Join-Path $adfRoot "trigger") -Filter *.json) {
  $raw = Get-Content $f.FullName -Raw | ConvertFrom-Json
  $trPath = Join-Path $env:TEMP "adf-tr-$($raw.name).json"
  $raw.properties | ConvertTo-Json -Depth 100 | Set-Content $trPath -Encoding utf8
  Write-Host "Trigger $($raw.name)"
  az datafactory trigger create -g $ResourceGroupName --factory-name $DataFactoryName --name $raw.name --properties "@$trPath" -o none
}
Write-Host "ADF artifact deployment finished."

# Ensure ADF MSI can invoke Databricks and read Key Vault secrets
$adfId = az datafactory show -g $ResourceGroupName -n $DataFactoryName --query identity.principalId -o tsv 2>$null
if ($adfId -and $dbwResourceId) {
  $existingDbw = az role assignment list --assignee $adfId --scope $dbwResourceId --query "[?roleDefinitionName=='Contributor'].id" -o tsv 2>$null
  if (-not $existingDbw) {
    Write-Host "Granting ADF MSI Contributor on Databricks workspace..."
    az role assignment create --assignee $adfId --role "Contributor" --scope $dbwResourceId -o none 2>$null
  }
}
if ($adfId -and $p.keyVaultName) {
  $kvId = az keyvault show -g $ResourceGroupName -n $p.keyVaultName --query id -o tsv 2>$null
  if ($kvId) {
    $existing = az role assignment list --assignee $adfId --scope $kvId --query "[?roleDefinitionName=='Key Vault Secrets User'].id" -o tsv 2>$null
    if (-not $existing) {
      Write-Host "Granting ADF MSI Key Vault Secrets User on $($p.keyVaultName)..."
      az role assignment create --assignee $adfId --role "Key Vault Secrets User" --scope $kvId -o none 2>$null
    }
  }
}



