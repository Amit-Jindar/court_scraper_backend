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
            case_type TEXT,
            case_number TEXT,
            case_year TEXT,
            status TEXT,
            petitioner TEXT,
            respondent TEXT,
            listing_date TEXT,
            court_no TEXT,
            orders_link TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")
