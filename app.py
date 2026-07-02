import sqlite3
from pathlib import Path
import streamlit as st


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "data" / "database" / "learning_os.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# LOAD CHAPTERS
# --------------------------------------------------

def get_chapters():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            chapter_title
        FROM chapters
        ORDER BY chapter_number
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_chapter_summary(chapter_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            chapter_title,
            summary_content
        FROM chapters
        WHERE id = ?
    """, (chapter_id,))

    row = cursor.fetchone()

    conn.close()

    return row


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="Learning OS",
    layout="wide"
)

st.title("📚 Learning OS")

chapters = get_chapters()

chapter_map = {
    title: chapter_id
    for chapter_id, title in chapters
}

selected_title = st.selectbox(
    "Select Chapter",
    options=list(chapter_map.keys())
)

chapter_id = chapter_map[selected_title]

chapter_title, summary_content = get_chapter_summary(
    chapter_id
)

st.divider()

st.header(chapter_title)

st.markdown(summary_content)