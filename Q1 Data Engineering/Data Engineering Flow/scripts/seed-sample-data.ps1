param(
  [string]$ProvisionedPath = (Join-Path $PSScriptRoot "..\infra\provisioned.dev.json"),
  [string]$SqlAdminPassword,
  [string]$PostgresAdminPassword,
  [switch]$DryRun
)
$ErrorActionPreference = "Stop"
function Invoke-AzQuiet([scriptblock]$Block) {
  $prev = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try { & $Block } finally { $ErrorActionPreference = $prev }
}
if (-not (Test-Path $ProvisionedPath)) { Write-Warning "Missing $ProvisionedPath - run provision first"; exit 0 }
$p = Get-Content $ProvisionedPath -Raw | ConvertFrom-Json
$root = Join-Path $PSScriptRoot ".."

Write-Host "Generating coherent retail SALES sample data..."
& python (Join-Path $PSScriptRoot "generate-sample-data.py")
& python (Join-Path $PSScriptRoot "seed\build-seed-from-csv.py")

$sample = Join-Path $root "data\sample"
if ($DryRun) {
  Write-Host "[DryRun] Would upload products.csv, customers.json; seed SQL, Postgres, Cosmos"
  exit 0
}

# Resolve passwords from Key Vault when not supplied
if (-not $SqlAdminPassword -and $p.keyVaultName) {
  $SqlAdminPassword = az keyvault secret show --vault-name $p.keyVaultName --name sql-admin-password --query value -o tsv 2>$null
}
if (-not $PostgresAdminPassword -and $p.keyVaultName) {
  $PostgresAdminPassword = az keyvault secret show --vault-name $p.keyVaultName --name postgres-admin-password --query value -o tsv 2>$null
}

# Blob: product catalog + REST customer JSON (sales cohort C0001-C0008)
Write-Host "Uploading product catalog and customer REST JSON to sources storage..."
Invoke-AzQuiet { az storage fs directory create --account-name $p.storageSourcesAccount --file-system $p.sourcesContainer --name customers -o none 2>$null }
Invoke-AzQuiet { az storage fs file upload --account-name $p.storageSourcesAccount --file-system $p.sourcesContainer --path "products/products.csv" --source (Join-Path $sample "products.csv") --auth-mode login -o none }
Invoke-AzQuiet { az storage fs file upload --account-name $p.storageSourcesAccount --file-system $p.sourcesContainer --path "customers/customers.json" --source (Join-Path $sample "customers.json") --auth-mode login -o none }

# Generate read SAS for ADF RestSource (private blob)
$expiry = (Get-Date).AddYears(2).ToString("yyyy-MM-dd")
$sas = Invoke-AzQuiet { az storage account generate-sas --account-name $p.storageSourcesAccount --services b --resource-types sco --permissions r --expiry $expiry -o tsv }
$restBase = "https://$($p.storageSourcesAccount).blob.core.windows.net/"
$restPath = "sources/customers/customers.json?$sas"
$p | Add-Member -NotePropertyName restCustomersBaseUrl -NotePropertyValue $restBase -Force
$p | Add-Member -NotePropertyName restCustomersPath -NotePropertyValue $restPath -Force
$p | Add-Member -NotePropertyName restCustomersApiUrl -NotePropertyValue $restBase -Force
$p | ConvertTo-Json -Depth 6 | Set-Content $ProvisionedPath -Encoding UTF8
Write-Host "REST customers URL (SAS) saved to provisioned.dev.json"

# SQL POS transactions (352 sales line items)
$sqlFile = Join-Path $PSScriptRoot "seed\pos_transactions.sql"
if (Test-Path $sqlFile) {
  $server = "$($p.sqlServer).database.windows.net"
  if (Get-Command sqlcmd -ErrorAction SilentlyContinue -and $SqlAdminPassword) {
    Write-Host "Seeding Azure SQL POS transactions..."
    sqlcmd -S $server -d $p.sqlDatabase -U $p.sqlAdminUser -P $SqlAdminPassword -i $sqlFile
  } else {
    Write-Host "Running Python SQL seed (sqlcmd unavailable)..."
    python (Join-Path $PSScriptRoot "seed\seed_sql_postgres.py") --target sql --server $server --database $p.sqlDatabase --user $p.sqlAdminUser --password $SqlAdminPassword --file $sqlFile
  }
}

# Postgres inventory (40 store x SKU rows tied to sales)
$pgFile = Join-Path $PSScriptRoot "seed\inventory.sql"
if (Test-Path $pgFile) {
  $pgHost = "$($p.postgresServer).postgres.database.azure.com"
  if (Get-Command psql -ErrorAction SilentlyContinue -and $PostgresAdminPassword) {
    Write-Host "Seeding PostgreSQL inventory snapshots..."
    $env:PGPASSWORD = $PostgresAdminPassword
    psql -h $pgHost -U $p.postgresAdminUser -d $p.postgresDatabase -f $pgFile
  } else {
    Write-Host "Running Python Postgres seed (psql unavailable)..."
    python (Join-Path $PSScriptRoot "seed\seed_sql_postgres.py") --target postgres --server $pgHost --database $p.postgresDatabase --user $p.postgresAdminUser --password $PostgresAdminPassword --file $pgFile
  }
}

# Cosmos store sales locations (S001-S005)
$cosmosScript = Join-Path $PSScriptRoot "seed\cosmos_stores.py"
if (Test-Path $cosmosScript) {
  Write-Host "Seeding Cosmos DB store metadata..."
  python $cosmosScript --account $p.cosmosAccount --database $p.cosmosDatabase --container $p.cosmosContainerStores --rg $p.resourceGroup --csv (Join-Path $sample "stores.csv")
}

Write-Host "Seed complete — 5 sources aligned: SQL POS, Blob products, REST customers, Postgres inventory, Cosmos stores."
