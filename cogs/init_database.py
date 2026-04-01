import os
import sys
import json

# Add parent directory to path to import database_manager
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Now import from cogs (since parent_dir is in path)
from cogs.database_manager import DatabaseManager

# Load config from parent directory
CONFIG_JSON = os.path.join(parent_dir, 'config.json')

with open(CONFIG_JSON, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# Extract variables from config
DB_FILE = config['paths'].get('database_file', 'database/user_database.db')
TEMPLATE_DIR = config['paths']['template_dir']
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'user_database_template.json')

print("[DatabaseInit] Initializing user database...")
print(f"[DatabaseInit] Database file: {DB_FILE}")
print(f"[DatabaseInit] Template file: {TEMPLATE_PATH}")

# Ensure database directory exists
db_dir = os.path.dirname(DB_FILE)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(f"[DatabaseInit] Created directory: {db_dir}")

try:
    # Initialize database
    db_manager = DatabaseManager(DB_FILE, TEMPLATE_PATH)
    print("[DatabaseInit] ✅ Database initialized successfully!")
    print(f"[DatabaseInit] Location: {os.path.abspath(DB_FILE)}")
    
    # Close connection
    db_manager.close()
    print("[DatabaseInit] Database connection closed.")
    
except FileNotFoundError as e:
    print(f"[DatabaseInit] ❌ Error: Template file not found!")
    print(f"[DatabaseInit] Expected location: {TEMPLATE_PATH}")
    sys.exit(1)
except Exception as e:
    print(f"[DatabaseInit] ❌ Error initializing database: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)