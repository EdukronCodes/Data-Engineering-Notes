<#
.SYNOPSIS
    Deploy Azure infrastructure (ADLS, Key Vault, ADF, Databricks) for retail pipeline.
.PARAMETER ResourceGroupName
    Target resource group (created if missing).
.PARAMETER ParametersFile
    Bicep parameters file path.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName,

    [string]$Location = "eastus",
    [string]$ParametersFile = "$PSScriptRoot\..\infra\parameters.dev.json"
)

$ErrorActionPreference = "Stop"
$infraDir = Join-Path $PSScriptRoot "..\infra"
$bicepFile = Join-Path $infraDir "main.bicep"

Write-Host "Checking Azure login..."
az account show | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Run 'az login' before deploying."
}

Write-Host "Ensuring resource group: $ResourceGroupName"
az group create --name $ResourceGroupName --location $Location | Out-Null

Write-Host "Deploying Bicep template..."
az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file $bicepFile `
    --parameters "@$ParametersFile" `
    --output table

Write-Host "Deployment complete. Capture outputs above for ADF/Databricks configuration."
