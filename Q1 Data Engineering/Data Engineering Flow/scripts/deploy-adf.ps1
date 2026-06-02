<#
.SYNOPSIS
    Deploy ADF artifacts to Azure Data Factory using ARM template or Az.DataFactory cmdlets.
.PARAMETER ResourceGroupName
    Resource group containing the Data Factory.
.PARAMETER DataFactoryName
    Name of the Azure Data Factory instance.
.PARAMETER Mode
    'arm' deploys ARMTemplateForFactory.json; 'git' prints git-integration steps only.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$ResourceGroupName,

    [Parameter(Mandatory = $true)]
    [string]$DataFactoryName,

    [ValidateSet("arm", "git")]
    [string]$Mode = "git"
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$factoryDir = Join-Path $root "adf\factory"

Write-Host "Azure Data Factory deployment — Mode: $Mode"

if ($Mode -eq "arm") {
    az account show | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Run 'az login' first." }

    $template = Join-Path $factoryDir "ARMTemplateForFactory.json"
    $params = Join-Path $factoryDir "ARMTemplateParametersForFactory.json"

    Write-Host "Deploying ARM template to $DataFactoryName..."
    az deployment group create `
        --resource-group $ResourceGroupName `
        --template-file $template `
        --parameters "@$params" `
        --parameters factoryName=$DataFactoryName `
        --output table

    Write-Host "ARM deployment submitted. Import remaining pipelines via Git integration (recommended)."
}
else {
    Write-Host @"

Git integration (recommended for full pipeline sync):
1. Push repo to Azure DevOps (scripts/push-to-azure-repos.ps1)
2. In ADF Studio: Manage > Git configuration
   - Repository: Azure DevOps Git
   - Project, repo, collaboration branch: main
   - Root folder: /adf
   - Publish branch: adf_publish
3. Publish from ADF UI to generate ARM in adf_publish branch
4. Use Azure DevOps release pipeline or az datafactory deploy to promote

Artifact folders in this repo:
  adf/linkedService/
  adf/dataset/
  adf/pipeline/
  adf/trigger/
  adf/factory/adf-retail-de.json

After Git connect, update linked service parameters for your storage accounts and Databricks cluster.
"@
}

# Optional: validate JSON artifacts locally
$validateScript = Join-Path $PSScriptRoot "validate-json.ps1"
if (Test-Path $validateScript) {
    & $validateScript
}
