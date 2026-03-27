# create_folder_structure.ps1
param(
    [string]$RootPath = (Get-Location),
    [switch]$Force
)

# Folder structuur
$FolderStructure = @(
    "cogs",
    "templates"
)

Write-Host "Creating folder structure at: $RootPath" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

foreach ($Folder in $FolderStructure) {
    $FullPath = Join-Path $RootPath $Folder
    
    try {
        if (Test-Path $FullPath) {
            if ($Force) {
                Write-Host "🔄 Folder exists, recreating: $Folder" -ForegroundColor Yellow
                Remove-Item -Path $FullPath -Recurse -Force
                New-Item -Path $FullPath -ItemType Directory -Force | Out-Null
            } else {
                Write-Host "⚠️  Already exists: $Folder" -ForegroundColor Yellow
            }
        } else {
            New-Item -Path $FullPath -ItemType Directory -Force | Out-Null
            Write-Host "✅ Created: $Folder" -ForegroundColor Green
        }
    } catch {
        Write-Host "❌ Error creating $Folder : $_" -ForegroundColor Red
    }
}

Write-Host "`n✅ Folder structure setup complete!" -ForegroundColor Green