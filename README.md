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


## Structure view 
```
 auto-discord-server-deployment/
├── setup.ps1                      # Main PowerShell setup script
├── setup_bot.py                   # Discord bot that configures the server
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .gitignore                     # Git ignore file
├── cogs/
│   ├── database_manager.py        # Database management class
│   └── init_database.py           # Database initialization script
└── templates/
    ├── moderation_template.json   # Moderation roles and channels template
    └── welcome_template.json      # Welcome channels template
'''

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