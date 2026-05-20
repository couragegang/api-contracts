# Lint OpenAPI specs (requires: npm i -g @redocly/cli)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $root

if (-not (Get-Command redocly -ErrorAction SilentlyContinue)) {
    Write-Host "Install: npm i -g @redocly/cli"
    exit 1
}

$specs = @("iam", "config", "mcp", "ai", "bff", "policy", "audit", "billing")
foreach ($s in $specs) {
    $path = Join-Path $root "$s/openapi.yaml"
    if (Test-Path $path) {
        Write-Host "Lint $s ..."
        redocly lint $path
    }
}
Write-Host "Done."
