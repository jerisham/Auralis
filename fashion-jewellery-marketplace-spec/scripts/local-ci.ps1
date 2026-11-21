# Local stand-in for the GitHub Actions job in .github/workflows/ci.yml.
# This does not protect main and does not deploy. V-20-02 still needs a remote
# that rejects a merge when this pipeline fails.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$timer = [Diagnostics.Stopwatch]::StartNew()

function Step($name, $command) {
    Write-Host ""
    Write-Host "== $name =="
    Invoke-Expression $command
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAILED: $name (exit $LASTEXITCODE)"
        exit $LASTEXITCODE
    }
}

Step "lint" "npx --yes pnpm@9.15.9 lint"
Step "typecheck" "npx --yes pnpm@9.15.9 typecheck"
Step "test" "npx --yes pnpm@9.15.9 test"
Step "build" "npx --yes pnpm@9.15.9 build"
Step "openapi" "npx --yes pnpm@9.15.9 --filter @auralis/api openapi:check"

$timer.Stop()
$minutes = [math]::Round($timer.Elapsed.TotalMinutes, 2)
Write-Host ""
Write-Host "Local CI finished in $minutes minutes."
if ($timer.Elapsed.TotalMinutes -gt 10) {
    Write-Host "Over the 10 minute budget in V-20-02."
    exit 1
}
