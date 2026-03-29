import sqlite3
import json
import os
from discord.ext import commands

# Load config
CONFIG_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

with open(CONFIG_JSON, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# Extract variables from config
DB_FILE = config['paths'].get('database_file', 'bot_database.db')
TEMPLATE_DIR = config['paths']['template_dir']

TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, 'user_database_template.json')


class DatabaseManager:
    def __init__(self, db_file, template_file):
        # Ensure database directory exists
        db_dir = os.path.dirname(db_file)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"[DatabaseManager] Created database directory: {db_dir}")
        
        # Convert to absolute path for clarity
        self.db_file = os.path.abspath(db_file)
        
        # Check if database file exists (for logging purposes)
        db_exists = os.path.exists(self.db_file)
        
        # Open sqlite synchronously (fine if used only in the bot's event loop)
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        
        if not db_exists:
            print(f"[DatabaseManager] Created new database file: {self.db_file}")
        else:
            print(f"[DatabaseManager] Connected to existing database: {self.db_file}")
        
        self.template = self._load_template(template_file)
        self._create_user_table()

    def _load_template(self, template_file):
        """Load JSON template for user DB."""
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"Template file not found: {template_file}")
        
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _create_user_table(self):
        """Create users table dynamically based on template."""
        user_fields = self.template.get("user", {})
        
        # Build column definitions dynamically from template
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        
        for field_name, default_value in user_fields.items():
            if field_name == "user_id":
                columns.append("user_id TEXT UNIQUE")
            elif isinstance(default_value, list):
                columns.append(f"{field_name} TEXT")  # Store arrays as JSON strings
            else:
                columns.append(f"{field_name} TEXT")
        
        create_sql = f"CREATE TABLE IF NOT EXISTS users ({', '.join(columns)})"
        
        self.cursor.execute(create_sql)
        self.connection.commit()
        print(f"[DatabaseManager] Table 'users' created/verified with structure: {columns}")

    def get_user(self, user_id: str):
        """Fetch a user by user_id."""
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def add_user(self, user_dict):
        """Add a user dynamically based on template fields."""
        user_fields = list(self.template.get("user", {}).keys())
        fields_str = ", ".join(user_fields)
        placeholders = ", ".join(["?" for _ in user_fields])
        values = [user_dict.get(field) for field in user_fields]
        
        self.cursor.execute(
            f"INSERT OR IGNORE INTO users ({fields_str}) VALUES ({placeholders})",
            values
        )
        self.connection.commit()

    def update_user(self, user_id: str, user_dict):
        """Update a user dynamically based on template fields."""
        user_fields = [f for f in self.template.get("user", {}).keys() if f != "user_id"]
        set_clause = ", ".join([f"{field}=?" for field in user_fields])
        values = [user_dict.get(field) for field in user_fields]
        values.append(user_id)
        
        self.cursor.execute(
            f"UPDATE users SET {set_clause} WHERE user_id=?",
            values
        )
        self.connection.commit()

    def delete_user(self, user_id: str):
        """Delete a user by user_id."""
        self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        self.connection.commit()

    def get_all_users(self):
        """Fetch all users."""
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def close(self):
        """Close the DB connection."""
        try:
            self.connection.close()
            print(f"[DatabaseManager] Database connection closed")
        except Exception as e:
            print(f"[DatabaseManager] Error closing database: {e}")


class DatabaseManagerCog(commands.Cog):
    def __init__(self, bot, db_manager: DatabaseManager):
        self.bot = bot
        self.db_manager = db_manager

    @commands.command()
    async def some_command(self, ctx):
        await ctx.send("This is a command from the Database Manager cog!")

    def cog_unload(self):
        # sync cleanup when cog is unloaded
        self.db_manager.close()


# Module-level async setup required by discord.py v2+
async def setup(bot):
    try:
        # instantiate DatabaseManager here (deferred from import time)
        db_manager = DatabaseManager(DB_FILE, TEMPLATE_PATH)
        await bot.add_cog(DatabaseManagerCog(bot, db_manager))
        print("[DatabaseManager] Cog loaded successfully")
    except FileNotFoundError as e:
        print(f"[DatabaseManager] Error loading cog: {e}")
        raise
    except Exception as e:
        print(f"[DatabaseManager] Unexpected error loading cog: {e}")
        raise