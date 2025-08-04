import sqlite3

DB_FILE = "cases.db"

def reset_database():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cases")
        conn.commit()
        conn.close()
        print("✅ Database cleaned successfully! All old cases removed.")
    except Exception as e:
        print("❌ Error while cleaning database:", e)

if __name__ == "__main__":
    reset_database()
