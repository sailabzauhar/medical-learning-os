import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "database" / "learning_os.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\nUSER_PROGRESS TABLE")

cursor.execute("PRAGMA table_info(user_progress)")

for row in cursor.fetchall():
    print(row)

conn.close()