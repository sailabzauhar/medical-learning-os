import os
import sqlite3
import psycopg2

from dotenv import load_dotenv

load_dotenv()

# ==================================================
# SQLITE
# ==================================================

SQLITE_DB = "data/database/learning_os.db"

sqlite_conn = sqlite3.connect(SQLITE_DB)
sqlite_cursor = sqlite_conn.cursor()

# ==================================================
# POSTGRES
# ==================================================

pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

pg_cursor = pg_conn.cursor()

# ==================================================
# LEGACY USER
# ==================================================

LEGACY_USER_ID = "00000000-0000-0000-0000-000000000001"

pg_cursor.execute("""
INSERT INTO users(
    id,
    email,
    name
)
VALUES(
    %s,
    %s,
    %s
)
ON CONFLICT (id)
DO NOTHING
""", (
    LEGACY_USER_ID,
    "legacy@learningos.local",
    "Legacy User"
))

pg_conn.commit()

# ==================================================
# BOOKS
# ==================================================

print("Migrating books...")

sqlite_cursor.execute("""
SELECT id, title
FROM books
""")

for row in sqlite_cursor.fetchall():

    pg_cursor.execute("""
    INSERT INTO books(
        id,
        title
    )
    VALUES (%s, %s)
    ON CONFLICT (id)
    DO NOTHING
    """, row)

pg_conn.commit()

# ==================================================
# CHAPTERS
# ==================================================

print("Migrating chapters...")

sqlite_cursor.execute("""
SELECT
    id,
    book_id,
    filename,
    chapter_number,
    chapter_title,
    summary_content,
    summary_word_count,
    mcq_count
FROM chapters
""")

for row in sqlite_cursor.fetchall():

    pg_cursor.execute("""
    INSERT INTO chapters(
        id,
        book_id,
        filename,
        chapter_number,
        chapter_title,
        summary_content,
        summary_word_count,
        mcq_count
    )
    VALUES (
        %s,%s,%s,%s,
        %s,%s,%s,%s
    )
    ON CONFLICT (id)
    DO NOTHING
    """, row)

pg_conn.commit()

# ==================================================
# MCQS
# ==================================================

print("Migrating mcqs...")

sqlite_cursor.execute("""
SELECT
    id,
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
FROM mcqs
""")

for row in sqlite_cursor.fetchall():

    pg_cursor.execute("""
    INSERT INTO mcqs(
        id,
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
    VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    ON CONFLICT (id)
    DO NOTHING
    """, row)

pg_conn.commit()

# ==================================================
# USER_PROGRESS
# ==================================================

print("Migrating user_progress...")

sqlite_cursor.execute("""
SELECT
    mcq_id,
    selected_answer,
    is_correct,
    attempted_at
FROM user_progress
""")

for row in sqlite_cursor.fetchall():

    pg_cursor.execute("""
    INSERT INTO user_progress(
        user_id,
        mcq_id,
        selected_answer,
        is_correct,
        attempted_at
    )
    VALUES (
        %s,%s,%s,%s,%s
    )
    """, (
        LEGACY_USER_ID,
        row[0],
        row[1],
        bool(row[2]),
        row[3]
    ))

pg_conn.commit()

# ==================================================
# MCQ_SRS
# ==================================================

print("Migrating mcq_srs...")

sqlite_cursor.execute("""
SELECT
    mcq_id,
    repetition,
    interval_days,
    ease_factor,
    last_reviewed,
    next_due
FROM mcq_srs
""")

for row in sqlite_cursor.fetchall():

    pg_cursor.execute("""
    INSERT INTO mcq_srs(
        user_id,
        mcq_id,
        repetition,
        interval_days,
        ease_factor,
        last_reviewed,
        next_due
    )
    VALUES(
        %s,%s,%s,%s,%s,%s,%s
    )
    ON CONFLICT (user_id, mcq_id)
    DO NOTHING
    """, (
        LEGACY_USER_ID,
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5]
    ))

pg_conn.commit()

# ==================================================
# VERIFY
# ==================================================

print("\nVerification")

for table in [
    "books",
    "chapters",
    "mcqs",
    "user_progress",
    "mcq_srs"
]:

    pg_cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = pg_cursor.fetchone()[0]

    print(table, count)

# ==================================================
# CLEANUP
# ==================================================

sqlite_conn.close()
pg_conn.close()

print("\nMigration Complete")