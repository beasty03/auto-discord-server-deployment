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

### 1. Install Python
- Download **Python 3.8 or higher** from [python.org](https://www.python.org/downloads/)
- **Important:** During installation, check **"Add Python to PATH"**

### 2. Install Required Python Packages
Open Command Prompt or PowerShell and run:
```bash
pip install discord.py aiohttp


## Structure view 

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


## First Run 

Right-click setup.ps1 → "Run with PowerShell"
