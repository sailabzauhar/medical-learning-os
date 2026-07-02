import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

JSON_DIR = BASE_DIR / "data" / "content"
DB_PATH = BASE_DIR / "data" / "database" / "learning_os.db"

BOOK_TITLE = "Standard Treatment Guidelines: A Manual for Medical Therapeutics (2013)"


def get_book_id(cursor):
    cursor.execute("""
        INSERT OR IGNORE INTO books(title)
        VALUES (?)
    """, (BOOK_TITLE,))

    cursor.execute("""
        SELECT id
        FROM books
        WHERE title = ?
    """, (BOOK_TITLE,))

    return cursor.fetchone()[0]


def insert_chapter(cursor, book_id, filename, data):

    chapter_number = None

    try:
        chapter_number = int(filename.split("_")[0])
    except:
        pass

    cursor.execute("""
        INSERT OR IGNORE INTO chapters(
            book_id,
            filename,
            chapter_number,
            chapter_title,
            summary_content,
            summary_word_count,
            mcq_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        book_id,
        filename,
        chapter_number,
        data["chapter_title"],
        data["summary"]["content"],
        data.get("summary_word_count", 0),
        data.get("mcq_count", 0)
    ))

    cursor.execute("""
        SELECT id
        FROM chapters
        WHERE filename = ?
    """, (filename,))

    return cursor.fetchone()[0]


def insert_mcqs(cursor, chapter_id, mcqs):

    inserted = 0

    for mcq in mcqs:

        explanation = mcq.get("explanation", {})
        incorrect = explanation.get("incorrect_options", {})

        cursor.execute("""
            INSERT OR IGNORE INTO mcqs(
                chapter_id,
                question_id,
                question,

                option_a,
                option_b,
                option_c,
                option_d,

                correct_answer,

                correct_reason,

                incorrect_a,
                incorrect_b,
                incorrect_c,
                incorrect_d,

                key_learning_point,

                difficulty,

                source_section
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (

            chapter_id,

            mcq.get("question_id"),

            mcq.get("question"),

            mcq["options"].get("A"),
            mcq["options"].get("B"),
            mcq["options"].get("C"),
            mcq["options"].get("D"),

            mcq.get("correct_answer"),

            explanation.get("correct_reason"),

            incorrect.get("A"),
            incorrect.get("B"),
            incorrect.get("C"),
            incorrect.get("D"),

            explanation.get("key_learning_point"),

            mcq.get("difficulty"),

            mcq.get("source_section")
        ))

        inserted += 1

    return inserted


def main():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    book_id = get_book_id(cursor)

    total_chapters = 0
    total_mcqs = 0

    json_files = sorted(JSON_DIR.glob("*.json"))

    print(f"Found {len(json_files)} JSON files\n")

    for json_file in json_files:

        print(f"Processing: {json_file.name}")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        chapter_id = insert_chapter(
            cursor,
            book_id,
            json_file.name,
            data
        )

        mcq_count = insert_mcqs(
            cursor,
            chapter_id,
            data.get("mcqs", [])
        )

        total_chapters += 1
        total_mcqs += mcq_count

    conn.commit()
    conn.close()

    print("\nMigration Complete")
    print(f"Chapters Processed: {total_chapters}")
    print(f"MCQs Processed: {total_mcqs}")


if __name__ == "__main__":
    main()