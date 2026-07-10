$ErrorActionPreference = "Stop"

$targets = Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -match "ai_media_lab\.lecture\.app:app" }

foreach ($target in $targets) {
  Stop-Process -Id $target.ProcessId -Force
  Write-Host "Stopped process $($target.ProcessId)"
}

if (!$targets) {
  Write-Host "No AI Lecture Note Taker server was running."
}

