import sqlite3
from pathlib import Path


def main():

    # Project root directory
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Database folder
    DB_DIR = BASE_DIR / "data" / "database"
    DB_DIR.mkdir(parents=True, exist_ok=True)

    # Database file
    DB_PATH = DB_DIR / "learning_os.db"

    print("\nCreating database...")
    print("Database path:")
    print(DB_PATH)
    print("\nAbsolute path:")
    print(DB_PATH.resolve())

    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # --------------------------------------------------
    # BOOKS
    # --------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE
    )
    """)

    # --------------------------------------------------
    # CHAPTERS
    # --------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        book_id INTEGER NOT NULL,

        filename TEXT NOT NULL UNIQUE,

        chapter_number INTEGER,

        chapter_title TEXT NOT NULL,

        summary_content TEXT NOT NULL,

        summary_word_count INTEGER,

        mcq_count INTEGER,

        UNIQUE(book_id, chapter_title),

        FOREIGN KEY(book_id)
            REFERENCES books(id)
    )
    """)

    # --------------------------------------------------
    # MCQS
    # --------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mcqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        chapter_id INTEGER NOT NULL,

        question_id INTEGER NOT NULL,

        question TEXT NOT NULL,

        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,

        correct_answer TEXT NOT NULL,

        correct_reason TEXT NOT NULL,

        incorrect_a TEXT,
        incorrect_b TEXT,
        incorrect_c TEXT,
        incorrect_d TEXT,

        key_learning_point TEXT,

        difficulty TEXT,

        source_section TEXT,

        UNIQUE(chapter_id, question_id),

        FOREIGN KEY(chapter_id)
            REFERENCES chapters(id)
    )
    """)

    # --------------------------------------------------
    # USER PROGRESS
    # --------------------------------------------------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        mcq_id INTEGER NOT NULL,

        selected_answer TEXT NOT NULL,

        is_correct INTEGER NOT NULL,

        attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(mcq_id)
            REFERENCES mcqs(id)
    )
    """)

    conn.commit()
    conn.close()

    print("\nDatabase created successfully.")
    print("File exists:", DB_PATH.exists())

    if DB_PATH.exists():
        print("Database size:", DB_PATH.stat().st_size, "bytes")


if __name__ == "__main__":
    main()