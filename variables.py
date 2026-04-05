# ============================================================================
# CONFIGURATION VARIABLES
# ============================================================================
#
# This file contains all configurable variables for the Discord bot.
# 
# IMPORTANT SECURITY NOTES:
# - Never commit this file with real tokens to GitHub!
# - Add variables.py to .gitignore
# - Use environment variables for production deployments
#
# HOW TO USE:
# 1. The setup.ps1 script will configure most of these automatically
# 2. For manual setup, fill in the values below
# 3. The launcher will automatically load these settings
#
# ============================================================================

from pathlib import Path
import os

# ============================================================================
# DISCORD BOT CONFIGURATION
# ============================================================================

# Your Discord Bot Token
# Get this from: https://discord.com/developers/applications
# Navigate to: Your App → Bot → Token
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Your Discord Server (Guild) ID
# Enable Developer Mode in Discord, then right-click your server → Copy ID
GUILD_ID = os.getenv("DISCORD_GUILD_ID", "YOUR_GUILD_ID_HERE")

# Bot Command Prefix
# The character(s) users type before commands (e.g., !help, ?help)
COMMAND_PREFIX = "!"

# Bot Status Message
# What the bot shows as "Playing..." or "Watching..."
BOT_STATUS = "!help for commands"
BOT_STATUS_TYPE = "watching"  # Options: playing, watching, listening, competing

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Enable/Disable logging to file
ENABLE_FILE_LOGGING = True

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = "INFO"

# Log file location
LOG_FILE = "bot.log"

# Maximum log file size (in bytes) before rotation
# 5MB = 5 * 1024 * 1024
MAX_LOG_SIZE = 5 * 1024 * 1024

# Number of backup log files to keep
LOG_BACKUP_COUNT = 3

# ============================================================================
# CHANNEL NAMES (for automated features)
# ============================================================================

# Channel where bot sends startup/shutdown notifications
LOG_CHANNEL_NAME = "moderator-only"

# Channel where welcome messages are sent
WELCOME_CHANNEL_NAME = "welcome"

# Channel for moderation logs (kicks, bans, warnings)
MOD_LOG_CHANNEL_NAME = "mod-logs"

# ============================================================================
# FEATURE TOGGLES
# ============================================================================

# Enable/Disable automatic welcome messages
ENABLE_WELCOME_MESSAGES = True

# Enable/Disable moderation logging
ENABLE_MOD_LOGGING = True

# Enable/Disable automatic role assignment on join
ENABLE_AUTO_ROLE = False

# Role name to auto-assign to new members (if enabled)
AUTO_ROLE_NAME = "Member"

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Database type: sqlite, postgresql, mysql
DATABASE_TYPE = "sqlite"

# SQLite database file path
SQLITE_DB_PATH = "database/user_database.db"

# PostgreSQL connection (if using PostgreSQL)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "discord_bot")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "discord_bot_db")

# ============================================================================
# PERMISSIONS & SECURITY
# ============================================================================

# User IDs that have bot owner privileges (can use dangerous commands)
# Add your Discord user ID here
BOT_OWNER_IDS = [
    # 123456789012345678,  # Example: Your Discord User ID
]

# Roles that can use admin commands (by role name)
ADMIN_ROLE_NAMES = ["Admin", "Administrator", "Owner"]

# Roles that can use moderator commands
MODERATOR_ROLE_NAMES = ["Moderator", "Mod", "Admin", "Administrator"]

# ============================================================================
# RATE LIMITING
# ============================================================================

# Maximum commands per user per minute (prevents spam)
MAX_COMMANDS_PER_MINUTE = 10

# Cooldown for specific heavy commands (in seconds)
HEAVY_COMMAND_COOLDOWN = 30

# ============================================================================
# EMBED COLORS (for pretty messages)
# ============================================================================

# Color codes in hexadecimal (0x prefix required)
COLOR_SUCCESS = 0x00FF00  # Green
COLOR_ERROR = 0xFF0000    # Red
COLOR_WARNING = 0xFFA500  # Orange
COLOR_INFO = 0x0099FF     # Blue
COLOR_NEUTRAL = 0x808080  # Gray

# ============================================================================
# PATHS (automatically configured)
# ============================================================================

# Base directory (where this file is located)
BASE_DIR = Path(__file__).parent

# Runtime cogs directory (loaded by launcher.py)
COGS_DIR = BASE_DIR / "cogs"

# Setup cogs directory (used only during initial setup)
SETUP_COGS_DIR = BASE_DIR / "setup_cogs"

# Templates directory
TEMPLATES_DIR = BASE_DIR / "templates"

# Database directory
DATABASE_DIR = BASE_DIR / "database"

# Logs directory
LOGS_DIR = BASE_DIR / "logs"

# Config file path
CONFIG_FILE = BASE_DIR / "config.json"

# ============================================================================
# AUTO-CREATE DIRECTORIES
# ============================================================================

def ensure_directories():
    """
    Creates necessary directories if they don't exist
    Called automatically when variables.py is imported
    """
    directories = [
        COGS_DIR,
        SETUP_COGS_DIR,
        TEMPLATES_DIR,
        DATABASE_DIR,
        LOGS_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Create directories on import
ensure_directories()

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """
    Validates that required configuration is set
    Returns list of errors if any
    """
    errors = []
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or not BOT_TOKEN:
        errors.append("BOT_TOKEN is not set in variables.py")
    
    if GUILD_ID == "YOUR_GUILD_ID_HERE" or not GUILD_ID:
        errors.append("GUILD_ID is not set in variables.py")
    
    if not COMMAND_PREFIX:
        errors.append("COMMAND_PREFIX cannot be empty")
    
    return errors

# ============================================================================
# EXPORT ALL SETTINGS
# ============================================================================

__all__ = [
    # Bot Config
    'BOT_TOKEN',
    'GUILD_ID',
    'COMMAND_PREFIX',
    'BOT_STATUS',
    'BOT_STATUS_TYPE',
    
    # Logging
    'ENABLE_FILE_LOGGING',
    'LOG_LEVEL',
    'LOG_FILE',
    'MAX_LOG_SIZE',
    'LOG_BACKUP_COUNT',
    
    # Channels
    'LOG_CHANNEL_NAME',
    'WELCOME_CHANNEL_NAME',
    'MOD_LOG_CHANNEL_NAME',
    
    # Features
    'ENABLE_WELCOME_MESSAGES',
    'ENABLE_MOD_LOGGING',
    'ENABLE_AUTO_ROLE',
    'AUTO_ROLE_NAME',
    
    # Database
    'DATABASE_TYPE',
    'SQLITE_DB_PATH',
    
    # Security
    'BOT_OWNER_IDS',
    'ADMIN_ROLE_NAMES',
    'MODERATOR_ROLE_NAMES',
    
    # Rate Limiting
    'MAX_COMMANDS_PER_MINUTE',
    'HEAVY_COMMAND_COOLDOWN',
    
    # Colors
    'COLOR_SUCCESS',
    'COLOR_ERROR',
    'COLOR_WARNING',
    'COLOR_INFO',
    'COLOR_NEUTRAL',
    
    # Paths
    'BASE_DIR',
    'COGS_DIR',
    'SETUP_COGS_DIR',
    'TEMPLATES_DIR',
    'DATABASE_DIR',
    'LOGS_DIR',
    'CONFIG_FILE',
    
    # Functions
    'validate_config',
]