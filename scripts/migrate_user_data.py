import os
import sqlite3
import psycopg2

from dotenv import load_dotenv

load_dotenv()

# ==================================================
# CONFIG
# ==================================================

SUPABASE_USER_ID = (
    "23f01e6b-6cec-4a68-8ff8-4cdb4a6df2f5"
)

# ==================================================
# SQLITE
# ==================================================

sqlite_conn = sqlite3.connect(
    "data/database/learning_os.db"
)

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
# CREATE USER PROFILE
# ==================================================

pg_cursor.execute("""
INSERT INTO users (
    id,
    email,
    name
)
VALUES (
    %s,
    %s,
    %s
)
ON CONFLICT (id)
DO NOTHING
""", (
    SUPABASE_USER_ID,
    "sailabzauhar@gmail.com",
    "Learning OS User"
))

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

rows = sqlite_cursor.fetchall()

for row in rows:

    pg_cursor.execute("""
    INSERT INTO user_progress (
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
        SUPABASE_USER_ID,
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

rows = sqlite_cursor.fetchall()

for row in rows:

    pg_cursor.execute("""
    INSERT INTO mcq_srs (
        user_id,
        mcq_id,
        repetition,
        interval_days,
        ease_factor,
        last_reviewed,
        next_due
    )
    VALUES (
        %s,%s,%s,%s,%s,%s,%s
    )
    ON CONFLICT (user_id, mcq_id)
    DO NOTHING
    """, (
        SUPABASE_USER_ID,
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

pg_cursor.execute("""
SELECT COUNT(*)
FROM user_progress
WHERE user_id = %s
""", (
    SUPABASE_USER_ID,
))

print(
    "user_progress",
    pg_cursor.fetchone()[0]
)

pg_cursor.execute("""
SELECT COUNT(*)
FROM mcq_srs
WHERE user_id = %s
""", (
    SUPABASE_USER_ID,
))

print(
    "mcq_srs",
    pg_cursor.fetchone()[0]
)

# ==================================================
# CLOSE
# ==================================================

sqlite_conn.close()
pg_conn.close()

print("\nUser migration complete.")