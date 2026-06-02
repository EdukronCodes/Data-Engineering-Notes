<#
.SYNOPSIS
    Upload sample retail CSV files to source ADLS for pipeline testing.
.PARAMETER StorageAccountName
    Source storage account name.
.PARAMETER Container
    Container name (default: sources).
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$StorageAccountName,

    [string]$Container = "sources"
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$sampleDir = Join-Path $root "data\sample"

# Generate sample data if missing
$genScript = Join-Path $PSScriptRoot "generate-sample-data.py"
if (-not (Test-Path (Join-Path $sampleDir "pos_transactions.csv"))) {
    python $genScript
}

$mapping = @{
    "pos_transactions.csv" = "pos_transactions"
    "inventory.csv"        = "inventory"
    "customers.csv"        = "customers"
    "products.csv"         = "products"
    "stores.csv"           = "stores"
}

az account show | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Run 'az login' first." }

foreach ($file in $mapping.Keys) {
    $localPath = Join-Path $sampleDir $file
    $destFolder = $mapping[$file]
    Write-Host "Uploading $file -> $Container/$destFolder/$file"
    az storage fs file upload `
        --account-name $StorageAccountName `
        --file-system $Container `
        --path "$destFolder/$file" `
        --source $localPath `
        --auth-mode login `
        --overwrite
}

Write-Host "Sample source files uploaded. Run pl_master_retail_pipeline in ADF."
