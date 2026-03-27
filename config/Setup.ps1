# Discord Server Setup Configuration Script
# This script generates a config.json file for automated Discord server setup

Write-Host "=== Discord Server Setup Configuration ===" -ForegroundColor Cyan
Write-Host ""

# Server Name
Write-Host ""
$serverName = Read-Host "Enter server name"

# Server Icon
Write-Host ""
Write-Host "Server Icon Options:" -ForegroundColor Yellow
Write-Host "1. Upload from file path"
Write-Host "2. Upload from URL"
$iconChoice = Read-Host "Choose option (or enter for no icon)"

$serverIcon = $null
$serverIconType = "none"

switch ($iconChoice) {
    "1" {
        $iconPath = Read-Host "Enter full path to image file (PNG/JPG/GIF)"
        if (Test-Path $iconPath) {
            $serverIcon = $iconPath
            $serverIconType = "file"
            Write-Host "Icon file found: $iconPath" -ForegroundColor Green
        } else {
            Write-Host "File not found. Skipping icon." -ForegroundColor Red
        }
    }
    "2" {
        $iconUrl = Read-Host "Enter image URL"
        $serverIcon = $iconUrl
        $serverIconType = "url"
        Write-Host "Icon URL set: $iconUrl" -ForegroundColor Green
    }
    default {
        Write-Host "No icon will be set." -ForegroundColor Yellow
    }
}

# Function to sanitize channel names (replace spaces with dashes)
function Format-ChannelName {
    param([string]$name)
    return $name.Trim() -replace '\s+', '-'
}

# Ask if welcome template should be included
Write-Host "Include Welcome Template?" -ForegroundColor Yellow
Write-Host "Note: Template creates member role and welcome setup for new users (optional)" -ForegroundColor Gray
$includeWelcome = Read-Host "Include welcome setup? (y/n)"
$useWelcomeTemplate = $includeWelcome -eq "y" -or $includeWelcome -eq "Y"

# Roles
Write-Host ""
Write-Host "custom roles..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Enter custom roles (comma-separated, e.g., Member,VIP,Guest):" -ForegroundColor Yellow
Write-Host "Note: Admin/Moderator roles are added automatically via the moderation template" -ForegroundColor Gray
$rolesInput = Read-Host "Custom roles"

if ([string]::IsNullOrWhiteSpace($rolesInput)) {
    $customRoles = @()
} else {
    $customRoles = @($rolesInput -split ',' | ForEach-Object { $_.Trim() })
}

# Categories and Channels
Write-Host ""
Write-Host "custom categories and channels..." -ForegroundColor Cyan
$categories = @()

do {
    Write-Host ""
    $categoryName = Read-Host "Enter category name (or press Enter to finish)" -ForegroundColor Yellow
    
    if ($categoryName -ne "") {
        Write-Host "Text channels for '$categoryName' (comma-separated):" -ForegroundColor Yellow
        $textChannelsInput = Read-Host "Text channels"
        
        # Create proper array from input
        if ([string]::IsNullOrWhiteSpace($textChannelsInput)) {
            $textChannels = @()
        } else {
            $textChannels = @($textChannelsInput -split ',' | ForEach-Object { 
                $trimmed = $_.Trim()
                if ($trimmed -ne "") { 
                    [PSCustomObject]@{
                        name = Format-ChannelName $trimmed
                    }
                }
            } | Where-Object { $_ -ne $null })
        }
        
        Write-Host "Voice channels for '$categoryName' (comma-separated):" -ForegroundColor Yellow
        $voiceChannelsInput = Read-Host "Voice channels"
        
        # Create proper array from input
        if ([string]::IsNullOrWhiteSpace($voiceChannelsInput)) {
            $voiceChannels = @()
        } else {
            $voiceChannels = @($voiceChannelsInput -split ',' | ForEach-Object { 
                $trimmed = $_.Trim()
                if ($trimmed -ne "") { 
                    [PSCustomObject]@{
                        name = Format-ChannelName $trimmed
                    }
                }
            } | Where-Object { $_ -ne $null })
        }
        
        # Show formatted channel names
        if ($textChannels.Count -gt 0) {
            Write-Host "  Text channels: $($textChannels.name -join ', ')" -ForegroundColor Gray
        }
        if ($voiceChannels.Count -gt 0) {
            Write-Host "  Voice channels: $($voiceChannels.name -join ', ')" -ForegroundColor Gray
        }
        
        # Force arrays in hashtable
        $category = [ordered]@{
            name = $categoryName
            text_channels = [array]$textChannels
            voice_channels = [array]$voiceChannels
        }
        
        $categories += $category
        Write-Host "Category '$categoryName' added!" -ForegroundColor Green
    }
} while ($categoryName -ne "")

# Build config object with proper structure
$config = [ordered]@{
    server = [ordered]@{
        name = $serverName
        icon = $serverIcon
        icon_type = $serverIconType
    }
    use_moderation_template = $true # Always include moderation template
    use_welcome_template = $useWelcomeTemplate
    custom_roles = [array]$customRoles
    custom_categories = [array]$categories
}

# Convert to JSON with proper array formatting
$jsonContent = $config | ConvertTo-Json -Depth 10 -Compress:$false

# Save to file
$configPath = Join-Path $PSScriptRoot "config.json"
$jsonContent | Out-File -FilePath $configPath -Encoding UTF8

Write-Host ""
Write-Host "=== Configuration saved to config.json ===" -ForegroundColor Green
Write-Host ""

if ($useWelcomeTemplate) {
    Write-Host "Welcome template will be applied with:" -ForegroundColor Cyan
    Write-Host "  - Member role (basic permissions)" -ForegroundColor Gray
    Write-Host "  - Welcome channel" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "Run: python setup_server.py"
