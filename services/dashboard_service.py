from services.db import (
    get_connection,
    release_connection
)


# ==================================================
# DASHBOARD METRICS
# ==================================================

def get_dashboard_metrics(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ------------------------------------------
        # TOTAL CHAPTERS
        # ------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM chapters
        """)

        total_chapters = cursor.fetchone()[0]

        # ------------------------------------------
        # COMPLETED CHAPTERS
        # ------------------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM (

                SELECT
                    c.id

                FROM chapters c

                JOIN mcqs m
                    ON c.id = m.chapter_id

                LEFT JOIN user_progress up
                    ON up.mcq_id = m.id
                   AND up.user_id = %s

                GROUP BY c.id

                HAVING COUNT(m.id) =
                       COUNT(up.id)

            ) completed
        """, (
            user_id,
        ))

        completed_chapters = cursor.fetchone()[0]

        # ------------------------------------------
        # ACCURACY
        # ------------------------------------------

        cursor.execute("""
            SELECT

                COUNT(*),
                COALESCE(
                    SUM(
                        CASE
                            WHEN is_correct THEN 1
                            ELSE 0
                        END
                    ),
                    0
                )

            FROM user_progress

            WHERE user_id = %s
        """, (
            user_id,
        ))

        total_attempts, correct_attempts = cursor.fetchone()

        accuracy = 0

        if total_attempts:

            accuracy = round(
                correct_attempts * 100 / total_attempts,
                1
            )

        # ------------------------------------------
        # CONCEPTS COVERED
        # ------------------------------------------

        cursor.execute("""
            SELECT
                COUNT(DISTINCT m.source_section)

            FROM mcqs m

            JOIN user_progress up
                ON up.mcq_id = m.id

            WHERE
                up.user_id = %s
            AND
                up.is_correct = TRUE
        """, (
            user_id,
        ))

        concepts_covered = cursor.fetchone()[0]

        return {

            "completed_chapters":
                completed_chapters,

            "total_chapters":
                total_chapters,

            "accuracy":
                accuracy,

            "concepts_covered":
                concepts_covered

        }

    finally:

        cursor.close()
        release_connection(conn)