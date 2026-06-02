<#
.SYNOPSIS
    Initialize git (if needed) and push retail pipeline to Azure DevOps Repos.
.PARAMETER RemoteUrl
    Azure DevOps Git remote URL, e.g.:
    https://dev.azure.com/myorg/myproject/_git/retail-data-engineering
.PARAMETER Branch
    Branch to push (default: main).
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$RemoteUrl,

    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..."
    git init
    git branch -M $Branch
}

Write-Host "Staging files (secrets excluded via .gitignore)..."
git add .
git status

$hasChanges = git diff --cached --quiet; $staged = $LASTEXITCODE -ne 0
if ($staged) {
    git commit -m "Initial retail data engineering pipeline (ADF + Databricks medallion)"
} else {
    Write-Host "No staged changes to commit."
}

$remotes = git remote
if ($remotes -notcontains "origin") {
    git remote add origin $RemoteUrl
} else {
    git remote set-url origin $RemoteUrl
}

Write-Host "Pushing to $RemoteUrl ($Branch)..."
git push -u origin $Branch

Write-Host @"

Next steps:
1. In Azure Data Factory Studio > Manage > Git configuration:
   - Repository type: Azure DevOps Git
   - Repository: select this repo
   - Root folder: /adf
   - Collaboration branch: $Branch
   - Publish branch: adf_publish
2. In Databricks > Repos > Add Repo > same Azure DevOps URL
3. Update infra/parameters.dev.json with your subscription values and redeploy if needed
"@
