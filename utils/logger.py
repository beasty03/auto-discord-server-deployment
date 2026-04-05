# ============================================================================
# LOGGING UTILITY
# ============================================================================
#
# Provides centralized logging for the entire bot
# Logs to both console and file with rotation
#
# ============================================================================

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

# Import configuration
try:
    from variables import (
        ENABLE_FILE_LOGGING,
        LOG_LEVEL,
        LOG_FILE,
        MAX_LOG_SIZE,
        LOG_BACKUP_COUNT,
        LOGS_DIR
    )
except ImportError:
    # Fallback defaults if variables.py doesn't exist
    ENABLE_FILE_LOGGING = True
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/bot.log"
    MAX_LOG_SIZE = 5 * 1024 * 1024
    LOG_BACKUP_COUNT = 3
    LOGS_DIR = Path("logs")

# ============================================================================
# LOGGER SETUP
# ============================================================================

def setup_logger(name: str = "discord_bot"):
    """
    Creates and configures a logger instance
    
    Args:
        name (str): Logger name (usually module name)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # ========================================
    # Console Handler (colored output)
    # ========================================
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Console format with colors
    console_format = ColoredFormatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # ========================================
    # File Handler (with rotation)
    # ========================================
    
    if ENABLE_FILE_LOGGING:
        # Ensure log directory exists
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        log_path = LOGS_DIR / LOG_FILE if not Path(LOG_FILE).is_absolute() else Path(LOG_FILE)
        
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=MAX_LOG_SIZE,
            backupCount=LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # File format (more detailed)
        file_format = logging.Formatter(
            '%(asctime)s | %(name)-20s | %(levelname)-8s | %(funcName)-20s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger

# ============================================================================
# COLORED CONSOLE OUTPUT
# ============================================================================

class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to console output
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def log_startup():
    """Logs bot startup information"""
    logger = logging.getLogger("discord_bot")
    logger.info("=" * 60)
    logger.info("BOT STARTING UP")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Log Level: {LOG_LEVEL}")
    logger.info(f"File Logging: {'Enabled' if ENABLE_FILE_LOGGING else 'Disabled'}")
    logger.info("=" * 60)

def log_shutdown():
    """Logs bot shutdown information"""
    logger = logging.getLogger("discord_bot")
    logger.info("=" * 60)
    logger.info("BOT SHUTTING DOWN")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Test the logger
    logger = setup_logger()
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")