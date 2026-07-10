param(
  [int]$Port = 8009
)

$ErrorActionPreference = "Stop"
$result = Invoke-RestMethod "http://127.0.0.1:$Port/api/health"
if ($result.status -ne "ok") {
  throw "Lecture app health check failed"
}
Write-Host "AI Lecture Note Taker is healthy."

