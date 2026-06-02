param(
  [string]$ConfigPath = (Join-Path $PSScriptRoot "..\infra\parameters.dev.json"),
  [switch]$DryRun,
  [switch]$SkipSeed,
  [string]$SqlAdminPassword,
  [string]$PostgresAdminPassword
)
$ErrorActionPreference = "Stop"
function Write-Step($m) { Write-Host "[$(Get-Date -Format HH:mm:ss)] $m" -ForegroundColor Cyan }
function Invoke-AzStep([string]$Label, [scriptblock]$Block) {
  Write-Step $Label
  if ($DryRun) { Write-Host "  [DryRun] would run" -ForegroundColor DarkGray; return $null }
  & $Block
}
if (-not (Get-Command az -ErrorAction SilentlyContinue)) { throw "Azure CLI (az) not found. Install: https://aka.ms/installazurecliwindows" }
$cfg = Get-Content $ConfigPath -Raw | ConvertFrom-Json
if ($cfg.subscriptionId) { az account set --subscription $cfg.subscriptionId | Out-Null }
$acct = az account show 2>$null | ConvertFrom-Json
if (-not $acct) { throw "Not logged in. Run: az login" }
Write-Step "Subscription: $($acct.name) ($($acct.id))"
$suffix = if ($FixedSuffix) { $FixedSuffix } elseif ($cfg.suffix) { $cfg.suffix } else { "" }
if (-not $suffix -and $cfg.useRandomSuffix) { $suffix = (Get-Random -Maximum 9999).ToString("0000") }
function N([string]$base) {
  $b = "$($cfg.namingPrefix)$base".ToLower() -replace '[^a-z0-9]',''
  if ($b.Length -gt 20) { $b = $b.Substring(0,20) }
  if ($suffix) { $b = "$b$suffix" }
  $b
}
$rg = $cfg.resourceGroup
$loc = $cfg.location
$dataLoc = if ($DataServicesLocation) { $DataServicesLocation } elseif ($cfg.dataServicesLocation) { $cfg.dataServicesLocation } else { $loc }
$tags = ($cfg.tags | ConvertTo-Json -Compress) -replace '"','\"'
$stLake = if ($cfg.storageLakeAccount) { N $cfg.storageLakeAccount.Replace('st','') ; "st$(N 'lake')" } else { "st$(N 'lake')" }
# simplify naming
$stLake = "st$($cfg.namingPrefix)lake$suffix".Substring(0,[Math]::Min(24,"st$($cfg.namingPrefix)lake$suffix".Length))
$stSrc  = "st$($cfg.namingPrefix)src$suffix".Substring(0,[Math]::Min(24,"st$($cfg.namingPrefix)src$suffix".Length))
$adfName = $cfg.dataFactoryName
if ($suffix -and $adfName -notmatch '\d{4}$') { $adfName = "$adfName$suffix" }
$kvName = "kv$($cfg.namingPrefix)$suffix".Replace('-','').Substring(0,[Math]::Min(24,"kv$($cfg.namingPrefix)$suffix".Replace('-','').Length))
$sqlServer = "$($cfg.sqlServerName)$suffix"
$pgServer = "$($cfg.postgresServerName)$suffix"
$cosmos = "$($cfg.cosmosAccountName)$suffix" -replace '[^a-z0-9-]',''
$dbw = "$($cfg.databricksWorkspaceName)$suffix"
if (-not $SqlAdminPassword) { $SqlAdminPassword = $env:SQL_ADMIN_PASSWORD }
if (-not $PostgresAdminPassword) { $PostgresAdminPassword = $env:POSTGRES_ADMIN_PASSWORD }
if (-not $SqlAdminPassword) { $SqlAdminPassword = -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 16 | ForEach-Object {[char]$_}) }
if (-not $PostgresAdminPassword) { $PostgresAdminPassword = -join ((48..57)+(65..90)+(97..122) | Get-Random -Count 16 | ForEach-Object {[char]$_}) }
$outPath = Join-Path $PSScriptRoot "..\infra\provisioned.dev.json"

Invoke-AzStep "Create resource group $rg" {
  az group create --name $rg --location $loc --tags project=retail-data-pipeline environment=$($cfg.environment) -o none
}

Invoke-AzStep "Create lake storage $stLake (ADLS Gen2)" {
  az storage account create -g $rg -n $stLake -l $loc --sku premium_LRS --kind StorageV2 --hns true -o none
  az storage container create --account-name $stLake --name $cfg.lakeContainer --auth-mode login -o none 2>$null
  foreach ($folder in $cfg.lakeFolders) {
    az storage fs directory create --account-name $stLake --file-system $cfg.lakeContainer --name $folder -o none
  }
}

Invoke-AzStep "Create sources storage $stSrc" {
  az storage account create -g $rg -n $stSrc -l $loc --sku premium_LRS --kind StorageV2 --hns true -o none
  az storage container create --account-name $stSrc --name $cfg.sourcesContainer --auth-mode login -o none 2>$null
  az storage fs directory create --account-name $stSrc --file-system $cfg.sourcesContainer --name products -o none
}

Invoke-AzStep "Create Key Vault $kvName" {
  az keyvault create -g $rg -n $kvName -l $loc --enable-rbac-authorization true -o none
}

Invoke-AzStep "Create SQL Server + database" {
  az sql server create -g $rg -n $sqlServer -l $dataLoc --admin-user $cfg.sqlAdminUser -p $SqlAdminPassword -o none
  az sql server firewall-rule create -g $rg -s $sqlServer -n AllowAzure --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0 -o none
  az sql db create -g $rg -s $sqlServer -n $cfg.sqlDatabaseName --service-objective Basic -o none
}

Invoke-AzStep "Create PostgreSQL Flexible Server + DB" {
  az postgres flexible-server create -g $rg -n $pgServer -l $dataLoc --sku-name Standard_B1ms --tier Burstable --storage-size 32 --version 16 --admin-user $cfg.postgresAdminUser --admin-password $PostgresAdminPassword --public-access 0.0.0.0 -o none
  az postgres flexible-server db create -g $rg -s $pgServer -d $cfg.postgresDatabaseName -o none
}

Invoke-AzStep "Create Cosmos DB account (stores metadata)" {
  az cosmosdb create -g $rg -n $cosmos --locations regionName=$dataLoc failoverPriority=0 isZoneRedundant=False -o none
  az cosmosdb sql database create -g $rg -a $cosmos -n $cfg.cosmosDatabaseName -o none
  az cosmosdb sql container create -g $rg -a $cosmos -d $cfg.cosmosDatabaseName -n $cfg.cosmosContainerStores --partition-key-path "/store_id" --throughput 400 -o none
}

Invoke-AzStep "Create Data Factory $adfName" {
  az datafactory create -g $rg -n $adfName -l $loc -o none
  $adfId = az datafactory show -g $rg -n $adfName --query identity.principalId -o tsv
  if ($adfId) {
    $lakeId = az storage account show -g $rg -n $stLake --query id -o tsv
    $srcId = az storage account show -g $rg -n $stSrc --query id -o tsv
    az role assignment create --assignee $adfId --role "Storage Blob Data Contributor" --scope $lakeId -o none 2>$null
    az role assignment create --assignee $adfId --role "Storage Blob Data Contributor" --scope $srcId -o none 2>$null
  }
}

Invoke-AzStep "Create Databricks workspace $dbw" {
  az databricks workspace create -g $rg -n $dbw -l $dataLoc --sku premium -o none
}

$lakeUrl = "https://$stLake.dfs.core.windows.net"
$srcUrl = "https://$stSrc.dfs.core.windows.net"
$dbwUrl = (az databricks workspace show -g $rg -n $dbw --query workspaceUrl -o tsv 2>$null); if (-not $dbwUrl) { $dbwUrl = "" }
$provisioned = [ordered]@{
  resourceGroup = $rg
  location = $loc
  suffix = $suffix
  storageLakeAccount = $stLake
  storageSourcesAccount = $stSrc
  lakeStorageAccountUrl = $lakeUrl
  sourceStorageAccountUrl = $srcUrl
  lakeContainer = $cfg.lakeContainer
  sourcesContainer = $cfg.sourcesContainer
  dataFactoryName = $adfName
  keyVaultName = $kvName
  keyVaultUrl = "https://$kvName.vault.azure.net/"
  sqlServer = $sqlServer
  sqlDatabase = $cfg.sqlDatabaseName
  sqlAdminUser = $cfg.sqlAdminUser
  postgresServer = $pgServer
  postgresDatabase = $cfg.postgresDatabaseName
  postgresAdminUser = $cfg.postgresAdminUser
  cosmosAccount = $cosmos
  cosmosDatabase = $cfg.cosmosDatabaseName
  cosmosContainerStores = $cfg.cosmosContainerStores
  databricksWorkspaceName = $dbw
  databricksWorkspaceUrl = $(if ($dbwUrl) { "https://$dbwUrl" } else { "" })
  restCustomersApiUrl = $cfg.restApiUrl
  deployedAt = (Get-Date).ToString("o")
}
$provisioned | ConvertTo-Json -Depth 5 | Set-Content $outPath -Encoding UTF8
Write-Step "Wrote $outPath"
if (-not $SkipSeed) {
  & (Join-Path $PSScriptRoot "seed-sample-data.ps1") -ProvisionedPath $outPath -SqlAdminPassword $SqlAdminPassword -PostgresAdminPassword $PostgresAdminPassword -DryRun:$DryRun
}
Write-Step "Provision complete."


