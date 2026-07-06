from datetime import date

from services.db import (
    get_connection,
    release_connection
)


# ==================================================
# DUE REVIEW COUNT
# ==================================================

def get_due_count(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        today = date.today()

        cursor.execute("""
            SELECT COUNT(*)
            FROM mcq_srs
            WHERE
                user_id = %s
            AND
                next_due <= %s
        """, (
            user_id,
            today
        ))

        return cursor.fetchone()[0]

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# NEXT DUE REVIEW
# ==================================================

def get_next_due_review(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        today = date.today()

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
                m.source_section,
                m.difficulty,
                c.chapter_title,
                s.next_due

            FROM mcqs m

            INNER JOIN mcq_srs s
                ON m.id = s.mcq_id

            INNER JOIN chapters c
                ON c.id = m.chapter_id

            WHERE

                s.user_id = %s

            AND

                s.next_due <= %s

            ORDER BY

                s.next_due ASC,
                m.question_id ASC

            LIMIT 1

        """, (
            user_id,
            today
        ))

        return cursor.fetchone()

    finally:

        cursor.close()
        release_connection(conn)