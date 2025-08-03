import sqlite3

DATABASE = "cases.db"

def get_db():
    """Connect to SQLite DB and return connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if not exists
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ctype TEXT,
            pet TEXT,
            orderdate TEXT,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()
