# Setup_infrastructure.ps1 - Quick installer

$repo = "https://github.com/beasty03/auto-discord-server-deployment.git"
$folder = "discord-server-setup"

Write-Host "=== Discord Server Setup Installer ===" -ForegroundColor Cyan

# Check Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git not installed! Download from: https://git-scm.com/downloads" -ForegroundColor Red
    exit 1
}

# Remove existing folder
if (Test-Path $folder) {
    Remove-Item $folder -Recurse -Force
}

# Clone
Write-Host "📥 Downloading..." -ForegroundColor Cyan
git clone $repo $folder

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Downloaded to: $folder" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. cd $folder" -ForegroundColor Gray
    Write-Host "2. Copy .env.example to .env" -ForegroundColor Gray
    Write-Host "3. Add your Discord token to .env" -ForegroundColor Gray
    Write-Host "4. Run: python setup_server.py" -ForegroundColor Gray
} else {
    Write-Host "❌ Download failed" -ForegroundColor Red
}
