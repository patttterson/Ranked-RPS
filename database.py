import sqlite3

def init_db():
    conn = sqlite3.connect("rps.db")
    cursor = conn.cursor()

    # Update users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        glicko_rating REAL DEFAULT 1500.0,
        glicko_rd REAL DEFAULT 350.0,
        glicko_volatility REAL DEFAULT 0.06
    )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect("rps.db")
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    init_db()
