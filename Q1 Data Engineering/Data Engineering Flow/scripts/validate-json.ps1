<#
.SYNOPSIS
    Validate all JSON artifacts under adf/ and databricks/jobs/.
#>
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$jsonFiles = @(
    Get-ChildItem -Path (Join-Path $root "adf") -Filter "*.json" -Recurse
    Get-ChildItem -Path (Join-Path $root "databricks\jobs") -Filter "*.json" -Recurse
    Get-ChildItem -Path (Join-Path $root "infra") -Filter "*.json" -Recurse
)

$failed = 0
foreach ($file in $jsonFiles) {
    try {
        Get-Content $file.FullName -Raw | ConvertFrom-Json | Out-Null
        Write-Host "[OK] $($file.FullName)"
    } catch {
        Write-Host "[FAIL] $($file.FullName): $_"
        $failed++
    }
}

if ($failed -gt 0) {
    throw "$failed JSON file(s) failed validation."
}

Write-Host "All $($jsonFiles.Count) JSON files valid."
