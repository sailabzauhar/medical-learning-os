from services.db import (
    get_connection,
    release_connection
)


# ==================================================
# CHAPTERS
# ==================================================

def get_chapters():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                id,
                chapter_title
            FROM chapters
            ORDER BY chapter_number
        """)

        rows = cursor.fetchall()

        return rows

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# PROGRESS
# ==================================================

def get_progress(
    chapter_id,
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # Total MCQs

        cursor.execute("""
            SELECT COUNT(*)
            FROM mcqs
            WHERE chapter_id = %s
        """, (
            chapter_id,
        ))

        total = cursor.fetchone()[0]

        # Introduced MCQs

        cursor.execute("""
            SELECT COUNT(DISTINCT s.mcq_id)
            FROM mcq_srs s
            JOIN mcqs m
                ON s.mcq_id = m.id
            WHERE
                s.user_id = %s
            AND
                m.chapter_id = %s
        """, (
            user_id,
            chapter_id
        ))

        introduced = cursor.fetchone()[0]

        return introduced, total

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# SAVE ATTEMPT
# ==================================================

def save_answer(
    user_id,
    mcq_id,
    selected_answer,
    correct_answer
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO user_progress (

                user_id,
                mcq_id,
                selected_answer,
                is_correct

            )
            VALUES (

                %s,
                %s,
                %s,
                %s

            )
        """, (

            user_id,
            mcq_id,
            selected_answer,
            selected_answer == correct_answer

        ))

        conn.commit()

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# RESET CHAPTER
# ==================================================

def reset_chapter(
    chapter_id,
    user_id
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            DELETE FROM user_progress
            WHERE
                user_id = %s
            AND
                mcq_id IN (

                    SELECT id
                    FROM mcqs
                    WHERE chapter_id = %s

                )
        """, (

            user_id,
            chapter_id

        ))

        cursor.execute("""
            DELETE FROM mcq_srs
            WHERE
                user_id = %s
            AND
                mcq_id IN (

                    SELECT id
                    FROM mcqs
                    WHERE chapter_id = %s

                )
        """, (

            user_id,
            chapter_id

        ))

        conn.commit()

    finally:

        cursor.close()
        release_connection(conn)