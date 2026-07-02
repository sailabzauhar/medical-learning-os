import sqlite3
from pathlib import Path
import streamlit as st

USER_ID = 1

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "database" / "learning_os.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# --------------------------------------------------
# CHAPTERS
# --------------------------------------------------

def get_chapters():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, chapter_title
        FROM chapters
        ORDER BY chapter_number
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# --------------------------------------------------
# FIND NEXT UNANSWERED MCQ
# --------------------------------------------------

def get_next_mcq(chapter_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.id,
            m.question,
            m.option_a,
            m.option_b,
            m.option_c,
            m.option_d,
            m.correct_answer,
            m.correct_reason,
            m.incorrect_a,
            m.incorrect_b,
            m.incorrect_c,
            m.incorrect_d,
            m.key_learning_point,
            m.source_section
        FROM mcqs m
        WHERE m.chapter_id = ?
        AND m.id NOT IN (
            SELECT mcq_id
            FROM user_progress
            WHERE user_id = ?
        )
        ORDER BY m.question_id
        LIMIT 1
    """, (chapter_id, USER_ID))

    row = cursor.fetchone()

    conn.close()

    return row


# --------------------------------------------------
# PROGRESS
# --------------------------------------------------

def get_progress(chapter_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM mcqs
        WHERE chapter_id = ?
    """, (chapter_id,))

    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM user_progress up
        JOIN mcqs m
            ON up.mcq_id = m.id
        WHERE up.user_id = ?
        AND m.chapter_id = ?
    """, (USER_ID, chapter_id))

    completed = cursor.fetchone()[0]

    conn.close()

    return completed, total


# --------------------------------------------------
# SAVE ANSWER
# --------------------------------------------------

def save_answer(mcq_id, selected, correct):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO user_progress(
            user_id,
            mcq_id,
            selected_answer,
            is_correct
        )
        VALUES (?, ?, ?, ?)
    """, (
        USER_ID,
        mcq_id,
        selected,
        int(selected == correct)
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# RESET CHAPTER
# --------------------------------------------------

def reset_chapter(chapter_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM user_progress
        WHERE user_id = ?
        AND mcq_id IN (
            SELECT id
            FROM mcqs
            WHERE chapter_id = ?
        )
    """, (USER_ID, chapter_id))

    conn.commit()
    conn.close()


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.title("📝 Chapter Quiz")

chapters = get_chapters()

chapter_map = {
    title: cid
    for cid, title in chapters
}

selected_title = st.selectbox(
    "Select Chapter",
    options=list(chapter_map.keys())
)

chapter_id = chapter_map[selected_title]

completed, total = get_progress(chapter_id)

st.info(f"Progress: {completed}/{total}")

col1, col2 = st.columns([3, 1])

with col2:

    if st.button("🔄 Reset Chapter Progress"):
        reset_chapter(chapter_id)
        st.success("Progress reset.")
        st.rerun()

mcq = get_next_mcq(chapter_id)

if mcq is None:

    st.success("🎉 Chapter completed!")

else:

    (
        mcq_id,
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
        source_section
    ) = mcq

    st.subheader(source_section)

    st.write(question)

    selected = st.radio(
        "Choose an answer",
        ["A", "B", "C", "D"],
        key=f"mcq_{mcq_id}"
    )

    option_map = {
        "A": option_a,
        "B": option_b,
        "C": option_c,
        "D": option_d
    }

    st.write(f"**A.** {option_a}")
    st.write(f"**B.** {option_b}")
    st.write(f"**C.** {option_c}")
    st.write(f"**D.** {option_d}")

    if st.button("Submit Answer"):

        save_answer(
            mcq_id,
            selected,
            correct_answer
        )

        if selected == correct_answer:
            st.success("✅ Correct")
        else:
            st.error(
                f"❌ Incorrect. Correct answer: {correct_answer}"
            )

        st.markdown("### Explanation")
        st.write(correct_reason)

        st.markdown("### Key Learning Point")
        st.write(key_learning_point)

        st.session_state["show_next"] = True

    if st.session_state.get("show_next", False):

        if st.button("Next Question"):

            st.session_state["show_next"] = False
            st.rerun()