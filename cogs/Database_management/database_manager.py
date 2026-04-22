import sqlite3
from pathlib import Path

# Fallback database path: discord-server-setup/database/user_database.db
_DEFAULT_DB = str(Path(__file__).parent.parent.parent / 'database' / 'user_database.db')

STARTING_BALANCE = 1000  # default starting balance for new users

class DatabaseManager:
    def __init__(self, db_path: str = _DEFAULT_DB, starting_balance: int = STARTING_BALANCE):
        self.db_path = db_path
        self.starting_balance = starting_balance
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_tables()

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
            cursor.execute('INSERT INTO casino (user_id, balance) VALUES (?, ?)', (user_id, self.starting_balance))
            conn.commit()
            conn.close()
            return self.starting_balance

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
