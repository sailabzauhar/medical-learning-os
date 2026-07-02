import sqlite3
from pathlib import Path
import streamlit as st

USER_ID = 1

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "database" / "learning_os.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

def get_dashboard_metrics():

    conn = get_connection()
    cursor = conn.cursor()

    # Total chapters
    cursor.execute("""
        SELECT COUNT(*)
        FROM chapters
    """)
    total_chapters = cursor.fetchone()[0]

    # Completed chapters
    cursor.execute("""
        SELECT COUNT(*)
        FROM (
            SELECT
                c.id
            FROM chapters c
            JOIN mcqs m
                ON c.id = m.chapter_id
            LEFT JOIN user_progress up
                ON m.id = up.mcq_id
                AND up.user_id = ?
            GROUP BY c.id
            HAVING COUNT(m.id) =
                   COUNT(up.id)
        )
    """, (USER_ID,))

    completed_chapters = cursor.fetchone()[0]

    # Accuracy
    cursor.execute("""
        SELECT
            COUNT(*),
            SUM(is_correct)
        FROM user_progress
        WHERE user_id = ?
    """, (USER_ID,))

    total_attempts, correct_attempts = cursor.fetchone()

    total_attempts = total_attempts or 0
    correct_attempts = correct_attempts or 0

    accuracy = 0

    if total_attempts > 0:
        accuracy = round(
            (correct_attempts / total_attempts) * 100,
            1
        )

    # Concepts covered
    cursor.execute("""
        SELECT COUNT(DISTINCT source_section)
        FROM mcqs m
        JOIN user_progress up
            ON up.mcq_id = m.id
        WHERE up.user_id = ?
        AND up.is_correct = 1
    """, (USER_ID,))

    concepts_covered = cursor.fetchone()[0]

    conn.close()

    return {
        "completed_chapters": completed_chapters,
        "total_chapters": total_chapters,
        "accuracy": accuracy,
        "concepts_covered": concepts_covered
    }


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.title("📊 Learning Dashboard")

metrics = get_dashboard_metrics()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Chapters Completed",
        f"{metrics['completed_chapters']}/{metrics['total_chapters']}"
    )

with col2:
    st.metric(
        "Concepts Covered",
        metrics["concepts_covered"]
    )

with col3:
    st.metric(
        "MCQ Accuracy",
        f"{metrics['accuracy']}%"
    )