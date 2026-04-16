import sqlite3
import sys
from pathlib import Path
from config_loader import load_config

# Load the configuration
config_file_path = str(Path(__file__).parent.parent.parent / 'config.json')  # Path to your config.json
config = load_config(config_file_path)

# Use the database path from the configuration
DATABASE_NAME = config["paths"]["database_file"]

# Add the casino folder to the path to import its variables
sys.path.insert(0, str(Path(__file__).parent.parent / 'casino'))
import variables as var  # Import casino-specific variables

class DatabaseManager:
    def __init__(self, db_path=DATABASE_NAME):
        self.db_path = db_path
        self.init_tables()  # Automatically create tables on initialization

    def init_tables(self):
        """Initialize the SQLite database and create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create the casino table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS casino (
                user_id INTEGER PRIMARY KEY,
                balance INTEGER NOT NULL DEFAULT 0,
                total_won INTEGER DEFAULT 0,
                total_lost INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                last_daily REAL DEFAULT 0,
                created_at REAL DEFAULT (julianday('now'))
            )
        ''')

        # Example for another table, e.g., a 'transactions' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                transaction_type TEXT,  -- 'deposit', 'withdraw', etc.
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES casino (user_id)
            )
        ''')

        conn.commit()
        conn.close()
        print(f"✅ Database initialized: {self.db_path}")

    # Example methods for interacting with the casino table
    def get_user_balance(self, user_id: int) -> int:
        """Get user balance, create account if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT balance FROM casino WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO casino (user_id, balance) VALUES (?, ?)', (user_id, var.STARTING_BALANCE))
            conn.commit()
            conn.close()
            return var.STARTING_BALANCE

        conn.close()
        return result[0]

    def update_balance(self, user_id: int, amount: int, won: bool = False):
        """Update user balance and statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if won:
            cursor.execute('''
                UPDATE casino 
                SET balance = balance + ?,
                    total_won = total_won + ?,
                    games_played = games_played + 1
                WHERE user_id = ?
            ''', (amount, amount, user_id))
        else:
            cursor.execute('''
                UPDATE casino 
                SET balance = balance - ?,
                    total_lost = total_lost + ?,
                    games_played = games_played + 1
                WHERE user_id = ?
            ''', (amount, amount, user_id))

        conn.commit()
        conn.close()

    def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT balance, total_won, total_lost, games_played, last_daily
            FROM casino WHERE user_id = ?
        ''', (user_id,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'balance': result[0],
                'total_won': result[1],
                'total_lost': result[2],
                'games_played': result[3],
                'last_daily': result[4]
            }
        return None

# Example of how to initialize the DatabaseManager in your cog file
if __name__ == "__main__":
    db_manager = DatabaseManager()