# Auto Discord Server Deployment

Automatically set up a complete Discord server with predefined roles, channels, categories, and moderation tools using a simple PowerShell script.

## Features

- Automated Server Setup - Configure your entire Discord server in minutes
- Role Management - Automatically create moderation roles with specific permissions
- Channel Organization - Set up categories, text channels, and voice channels
- Moderation Tools - Built-in moderation template with logs and reports
- Welcome System - Optional welcome channels and roles
- User Database - SQLite database for tracking user data
- Customizable - Add your own roles, categories, and channels


## Prerequisites

### 1. Install Python (use Microsoft Store)
- Open **Microsoft Store** on Windows
- Search for **"Python install manager"** (or latest version available)
- Click **"Get"**
- **Add python to PATH y/N: yes**

**Alternative:** Download from [python.org](https://www.python.org/downloads/)
- **Important:** During installation, check **"Add Python to PATH"**

### 2. Install Git
- Download **Git** from [git-scm.com/downloads](https://git-scm.com/downloads)
- Run the installer with default settings
- Restart PowerShell after installation

### 3. Install Required Python Packages
Open Command Prompt or PowerShell and run:
```bash
pip install discord.py aiohttp
```

## Structure view 
```
 auto-discord-server-deployment/
├── setup.ps1                         # Main PowerShell setup script
├── setup_bot.py                      # Bot config and Cog importation
├── README.md                         # information file
├── cogs/
│   ├──  Welcome (example)            # Imported script folder
│   │     ├── Script.py               # Main script file
│   │     ├── variables.py            # Main script variables file
│   │     └── README.md               # Information about imported script
│   └──  ...
│
├── setup_cogs/
│   ├── database_manager.py           # Database management class
│   ├── generate_invite.py            # Setup bot invite to server script        
│   └── init_database.py              # Database initialization script
│
├── templates/
│   ├── moderation_template.json      # Moderation roles and channels template
│   ├── user_database_template.json   # database template
│   └── welcome_template.json         # Welcome channels template
│
├── utils/
│   ├── config_loader.py              # Moderation roles and channels template
│   └── logger.py                     # database template
│
├── database/                         # folder location for database (will be created automaticaly)
│
├── config.json                       # information file
├── Setup_server.py                   # information file
├── launcher.py                       # information file
```

## First Run 

- Create a folder where you would like to keep your data 
- Download the setup powershell script from the repo: link repo
- Place the script in the folder 
- Right-click setup.ps1 → ``` "Run with PowerShell" ```

## Recommended Development Environment

### Visual Studio Code (Optional but Recommended)

**Why VS Code?**
- Built-in terminal for running scripts
- Syntax highlighting for Python and PowerShell
- IntelliSense for code completion
- Integrated Git support
- Easy file management

#### Install VS Code
1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Run the installer with default settings
3. Launch VS Code

#### Required Extensions

Install these extensions for the best development experience:

**Python Development:**
- **Python** (by Microsoft) - Python language support
  - Extension ID: `ms-python.python`
  - Provides IntelliSense, debugging, and code formatting

**PowerShell Support:**
- **PowerShell** (by Microsoft) - PowerShell language support
  - Extension ID: `ms-vscode.powershell`
  - Syntax highlighting and script debugging

**Additional Recommended Extensions:**
- **GitLens** (by GitKraken) - Enhanced Git integration
  - Extension ID: `eamodio.gitlens`
  - View commit history and blame annotations

- **Discord Presence** (by iCrawl) - Show what you're working on in Discord
  - Extension ID: `icrawl.discord-vscode`
  - Optional: Display your coding activity

- **Error Lens** (by Alexander) - Highlight errors inline
  - Extension ID: `usernamehw.errorlens`
  - See errors and warnings directly in your code

#### How to Install Extensions

**Method 1: Through VS Code**
1. Open VS Code
2. Click the **Extensions** icon in the sidebar (or press `Ctrl+Shift+X`)
3. Search for the extension name
4. Click **Install**



# COG DEVELOPMENT GUIDE
 
This guide ensures consistency and proper functionality when creating new cogs for the Discord bot.
 
---
 
## 📋 TABLE OF CONTENTS
 
1. [File Structure](#file-structure)
2. [Required Imports](#required-imports)
3. [Configuration Setup](#configuration-setup)
4. [Database Setup (Optional)](#database-setup-optional)
5. [Cog Class Structure](#cog-class-structure)
6. [Setup Function](#setup-function)
7. [Command Best Practices](#command-best-practices)
8. [Error Handling](#error-handling)
9. [Logging](#logging)
10. [Testing Checklist](#testing-checklist)
11. [Examples](#examples)
 
---
 
## 📁 FILE STRUCTURE
 
### Standard Cog Location
 
### Naming Conventions
- **Folder names**: PascalCase (e.g., `Casino`, `Moderation`)
- **File names**: snake_case (e.g., `gamble.py`, `blackjack.py`)
- **Class names**: PascalCase + "Cog" suffix (e.g., `GambleCog`, `BlackjackCog`)
 
---
 
## 📦 REQUIRED IMPORTS
 
### Minimum Required Imports
```python
import discord
from discord.ext import commands
from discord import app_commands
import sys
from pathlib import Path
 ```
# Add current folder to path for importing variables
```sys.path.insert(0, str(Path(__file__).parent))
import variables as var
import sqlite3          # For database operations
import random           # For random elements
import time             # For cooldowns/timestamps
from datetime import datetime, timedelta  # For time-based features
import asyncio          # For async operations
```
# variables.py
 ```
from utils.config_loader import get_bot_token, load_config
from pathlib import Path
 
# ============================================================================
# CENTRAL CONFIG LOADER
# ============================================================================
 
# Load bot token and config from central config.json
BOT_TOKEN = get_bot_token()  # or get_bot_token('SpecificBotName')
config = load_config()
GUILD_ID = int(config['guild_id'])
SERVER_NAME = config['server_name']
 
# Database path from config (nested under 'paths')
if 'paths' in config:
    paths = config['paths']
    if 'database_file' in paths:
        DATABASE_NAME = str(Path(paths['database_file']))
    elif 'db_file' in paths:
        DATABASE_NAME = str(Path(paths['db_file']))
    else:
        # Fallback
        PROJECT_ROOT = Path(__file__).parent.parent.parent
        DATABASE_DIR = PROJECT_ROOT / 'database'
        DATABASE_DIR.mkdir(exist_ok=True)
        DATABASE_NAME = str(DATABASE_DIR / 'user_database.db')
else:
    # Fallback
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATABASE_DIR = PROJECT_ROOT / 'database'
    DATABASE_DIR.mkdir(exist_ok=True)
    DATABASE_NAME = str(DATABASE_DIR / 'user_database.db')
 
# ============================================================================
# YOUR COG-SPECIFIC SETTINGS
# ============================================================================
 
# Example settings
FEATURE_ENABLED = True
MAX_VALUE = 1000
MIN_VALUE = 10
COOLDOWN_SECONDS = 5
 
# Embed Colors (in hex)
COLOR_SUCCESS = 0x00FF00  # Green
COLOR_ERROR = 0xFF0000    # Red
COLOR_WARNING = 0xFFA500  # Orange
COLOR_INFO = 0x00BFFF     # Light Blue
 
# Messages
MESSAGE_SUCCESS = "Operation completed successfully!"
MESSAGE_ERROR = "An error occurred!"
import sys
from pathlib import Path
 ```
# Add Casino folder to path to import variables.py
```
sys.path.insert(0, str(Path(__file__).parent))
import variables as var
def init_database():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(var.DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS your_table_name (
            user_id INTEGER PRIMARY KEY,
            data_field TEXT NOT NULL,
            counter INTEGER DEFAULT 0,
            created_at REAL DEFAULT (julianday('now'))
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ Database initialized: {var.DATABASE_NAME}")
def get_user_data(user_id: int):
    """Get user data from database."""
    conn = sqlite3.connect(var.DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM your_table_name WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result
 
def update_user_data(user_id: int, str):
    """Update user data in database."""
    conn = sqlite3.connect(var.DATABASE_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO your_table_name (user_id, data_field)
        VALUES (?, ?)
    ''', (user_id, data))
    
    conn.commit()
    conn.close()
class YourCog(commands.Cog):
    """Brief description of what this cog does."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Initialize any instance variables here
    
    @app_commands.command(
        name="commandname",
        description="What this command does"
    )
    @app_commands.describe(
        parameter="Description of this parameter"
    )
    async def command_name(
        self, 
        interaction: discord.Interaction, 
        parameter: str
    ):
        """Command implementation."""
        
        # Your command logic here
        
        embed = discord.Embed(
            title="Title",
            description="Description",
            color=var.COLOR_SUCCESS
        )
        
        await interaction.response.send_message(embed=embed)
async def setup(bot: commands.Bot):
    """
    Setup function to load this cog.
    Required for the launcher to load this module.
    """
    # Initialize database (if needed)
    # init_database()
    
    # Add the cog to the bot
    await bot.add_cog(YourCog(bot))
    
    print("✅ YourCategory/YourCog loaded successfully")
embed = discord.Embed(
    title="Command Title",
    description="Main message",
    color=var.COLOR_SUCCESS
)
 
embed.add_field(name="Field Name", value="Field Value", inline=True)
embed.set_footer(text=f"Requested by {interaction.user.display_name}")
embed.timestamp = datetime.utcnow()
 
await interaction.response.send_message(embed=embed)
await interaction.response.send_message(
    embed=error_embed, 
    ephemeral=True  # Only visible to user
)
@app_commands.command(name="command")
@app_commands.checks.cooldown(1, 60.0)  # 1 use per 60 seconds
async def command(self, interaction: discord.Interaction):
    # Command logic
    pass
@app_commands.command(name="command")
async def command(self, interaction: discord.Interaction):
    # Defer response if operation takes > 3 seconds
    await interaction.response.defer()
    
    # Do long operation
    await asyncio.sleep(5)
    
    # Send follow-up
    await interaction.followup.send(embed=embed)
if amount <= 0:
    embed = discord.Embed(
        title="❌ Invalid Input",
        description="Amount must be positive!",
        color=var.COLOR_ERROR
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)
    return
@command_name.error
async def command_error(self, interaction: discord.Interaction, error):
    """Handle errors for this specific command."""
    
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = discord.Embed(
            title="⏰ Cooldown Active",
            description=f"Try again in {error.retry_after:.1f} seconds",
            color=var.COLOR_WARNING
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(
            title="❌ Error",
            description=f"An error occurred: {str(error)}",
            color=var.COLOR_ERROR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
async def cog_app_command_error(
    self, 
    interaction: discord.Interaction, 
    error: app_commands.AppCommandError
):
    """Handle all errors in this cog."""
    
    if isinstance(error, app_commands.CommandOnCooldown):
        # Handle cooldown
        pass
    elif isinstance(error, app_commands.MissingPermissions):
        # Handle permissions
        pass
    else:
        # Generic error
        pass
from utils.logger import setup_logger
 
logger = setup_logger(__name__)
 ```
# In your commands
```
logger.info(f"User {interaction.user} used command /commandname")
logger.error(f"Error in command: {str(error)}")
logger.warning(f"Warning: unusual behavior detected")
import discord
from discord.ext import commands
from discord import app_commands
import sys
from pathlib import Path
 
sys.path.insert(0, str(Path(__file__).parent))
import variables as var
 
class PingCog(commands.Cog):
    """Simple ping command."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Ping command."""
        
        latency = round(self.bot.latency * 1000)
        
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: **{latency}ms**",
            color=var.COLOR_SUCCESS
        )
        
        await interaction.response.send_message(embed=embed)
 
async def setup(bot: commands.Bot):
    await bot.add_cog(PingCog(bot))
    print("✅ Utility/Ping cog loaded successfully")
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import sys
from pathlib import Path
 
sys.path.insert(0, str(Path(__file__).parent))
import variables as var
 
def init_database():
    conn = sqlite3.connect(var.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_points (
            user_id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
 
def add_points(user_id: int, points: int):
    conn = sqlite3.connect(var.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_points (user_id, points) 
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET points = points + ?
    ''', (user_id, points, points))
    conn.commit()
    conn.close()
 
class PointsCog(commands.Cog):
    """Points system."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="addpoints", description="Add points to user")
    @app_commands.describe(amount="Number of points to add")
    async def addpoints(self, interaction: discord.Interaction, amount: int):
        """Add points command."""
        
        if amount <= 0:
            embed = discord.Embed(
                title="❌ Invalid Amount",
                description="Points must be positive!",
                color=var.COLOR_ERROR
            )
            await interaction
```