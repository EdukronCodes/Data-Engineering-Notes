param(
  [string]$ProvisionedPath = (Join-Path $PSScriptRoot "..\infra\provisioned.dev.json")
)
$ErrorActionPreference = "Stop"
$p = Get-Content $ProvisionedPath -Raw | ConvertFrom-Json
$pgPwd = az keyvault secret show --vault-name $p.keyVaultName --name postgres-admin-password --query value -o tsv
if (-not $pgPwd) { throw "Could not read postgres-admin-password from $($p.keyVaultName)" }

$props = @{
  type = 'PostgreSqlV2'
  description = 'Inventory snapshots in PostgreSQL Flexible Server'
  server = "$($p.postgresServer).postgres.database.azure.com"
  port = 5432
  database = $p.postgresDatabase
  username = $p.postgresAdminUser
  password = @{ type = 'SecureString'; value = $pgPwd }
  sslMode = 'VerifyFull'
  authenticationType = 'Basic'
}
$path = Join-Path $env:TEMP "ls-postgresql-fix.json"
$props | ConvertTo-Json -Depth 5 | Set-Content $path -Encoding utf8

Write-Host "Updating ls_postgresql_inventory with Key Vault password..."
az datafactory linked-service create -g $p.resourceGroup --factory-name $p.dataFactoryName --name ls_postgresql_inventory --properties "@$path" -o none
Write-Host "Done. Test with: .\scripts\run-adf-master.ps1 -Wait"
