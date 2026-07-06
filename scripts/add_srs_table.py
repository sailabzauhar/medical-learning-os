import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "database" / "learning_os.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mcq_srs (

    user_id INTEGER NOT NULL,

    mcq_id INTEGER NOT NULL,

    repetition INTEGER NOT NULL DEFAULT 0,

    interval_days INTEGER NOT NULL DEFAULT 0,

    ease_factor REAL NOT NULL DEFAULT 2.5,

    last_reviewed DATE,

    next_due DATE,

    PRIMARY KEY(user_id, mcq_id),

    FOREIGN KEY(mcq_id)
        REFERENCES mcqs(id)
)
""")

conn.commit()
conn.close()

print("mcq_srs table created successfully.")