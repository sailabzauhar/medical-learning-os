from datetime import date

from services.db import (
    get_connection,
    release_connection
)


# ==================================================
# SUBTOPICS
# ==================================================

def get_subtopics(chapter_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                source_section,
                COUNT(*),
                MIN(question_id) AS first_question
            FROM mcqs
            WHERE chapter_id = %s
            GROUP BY source_section
            ORDER BY first_question
        """, (chapter_id,))

        rows = [
            (row[0], row[1])
            for row in cursor.fetchall()
        ]

        return rows

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# DUE REVIEW
# ==================================================

def get_due_review(
    chapter_id,
    user_id,
    source_section=None
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        today = date.today()

        sql = """
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
                m.source_section,
                m.difficulty
            FROM mcqs m
            JOIN mcq_srs s
                ON m.id = s.mcq_id
            WHERE
                m.chapter_id = %s
            AND
                s.user_id = %s
            AND
                s.next_due <= %s
        """

        params = [
            chapter_id,
            user_id,
            today
        ]

        if source_section:

            sql += """
                AND m.source_section = %s
            """

            params.append(source_section)

        sql += """
            ORDER BY
                s.next_due,
                m.question_id
            LIMIT 1
        """

        cursor.execute(sql, tuple(params))

        return cursor.fetchone()

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# NEW QUESTION
# ==================================================

def get_new_question(
    chapter_id,
    user_id,
    source_section=None
):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        sql = """
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
                m.source_section,
                m.difficulty
            FROM mcqs m
            WHERE
                m.chapter_id = %s
            AND
                m.id NOT IN (

                    SELECT mcq_id
                    FROM mcq_srs
                    WHERE user_id = %s

                )
        """

        params = [
            chapter_id,
            user_id
        ]

        if source_section:

            sql += """
                AND m.source_section = %s
            """

            params.append(source_section)

        sql += """
            ORDER BY
                m.question_id
            LIMIT 1
        """

        cursor.execute(sql, tuple(params))

        return cursor.fetchone()

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# LEARNING QUEUE
# ==================================================

def get_learning_mcq(
    chapter_id,
    user_id,
    source_section=None
):

    due = get_due_review(
        chapter_id,
        user_id,
        source_section
    )

    if due:
        return due, "review"

    new_question = get_new_question(
        chapter_id,
        user_id,
        source_section
    )

    if new_question:
        return new_question, "new"

    return None, None