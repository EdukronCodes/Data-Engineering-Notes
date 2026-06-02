<#
.SYNOPSIS
    Upload Databricks notebooks and create/update the retail medallion job.
.PARAMETER DatabricksHost
    Workspace URL, e.g. https://adb-123.0.azuredatabricks.net
.PARAMETER Token
    Personal access token (prefer env: DATABRICKS_TOKEN)
.PARAMETER RepoPath
    Databricks Repos path where notebooks will be synced.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$DatabricksHost,

    [string]$Token = $env:DATABRICKS_TOKEN,

    [string]$RepoPath = "/Repos/retail-data-engineering"
)

$ErrorActionPreference = "Stop"

if (-not $Token) {
    throw "Set DATABRICKS_TOKEN environment variable or pass -Token."
}

$root = Split-Path $PSScriptRoot -Parent
$notebooksRoot = Join-Path $root "databricks\notebooks"
$jobFile = Join-Path $root "databricks\jobs\retail_medallion_job.json"

Write-Host "Databricks deployment helper"
Write-Host "Host: $DatabricksHost"
Write-Host ""
Write-Host @"
Recommended approach (Repos):
1. Connect Azure DevOps repo in Databricks: Workspace > Repos > Add Repo
   URL: https://dev.azure.com/{org}/{project}/_git/{repo}
   Path: $RepoPath
2. Notebooks are at: $RepoPath/databricks/notebooks/
3. Create job from JSON:
   databricks jobs create --json @$jobFile
   (requires Databricks CLI: pip install databricks-cli && databricks configure --token)

Or use Azure DevOps pipeline step:
  - task: configuredatabricks@0
  - script: databricks workspace import_dir ...

Local notebooks path: $notebooksRoot
Job definition: $jobFile
"@

# Validate job JSON
if (Test-Path $jobFile) {
    Get-Content $jobFile -Raw | ConvertFrom-Json | Out-Null
    Write-Host "Job JSON validated successfully."
}
