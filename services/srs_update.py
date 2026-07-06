from services.db import (
    get_connection,
    release_connection
)

from services.sm2 import sm2_review


# ==================================================
# UPDATE SRS
# ==================================================

def update_srs(
    user_id,
    mcq_id,
    quality
):
    """
    Create or update SM-2 state for a MCQ.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ==================================================
        # EXISTING STATE
        # ==================================================

        cursor.execute("""
            SELECT
                repetition,
                interval_days,
                ease_factor
            FROM mcq_srs
            WHERE
                user_id = %s
            AND
                mcq_id = %s
        """, (
            user_id,
            mcq_id
        ))

        row = cursor.fetchone()

        if row is None:

            repetition = 0
            interval_days = 0
            ease_factor = 2.5

        else:

            repetition = row[0]
            interval_days = row[1]
            ease_factor = row[2]

        # ==================================================
        # RUN SM-2
        # ==================================================

        result = sm2_review(
            repetition=repetition,
            interval_days=interval_days,
            ease_factor=ease_factor,
            quality=quality
        )

        # ==================================================
        # UPSERT
        # ==================================================

        cursor.execute("""
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

                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s

            )

            ON CONFLICT (user_id, mcq_id)

            DO UPDATE SET

                repetition =
                    EXCLUDED.repetition,

                interval_days =
                    EXCLUDED.interval_days,

                ease_factor =
                    EXCLUDED.ease_factor,

                last_reviewed =
                    EXCLUDED.last_reviewed,

                next_due =
                    EXCLUDED.next_due
        """, (

            user_id,
            mcq_id,
            result["repetition"],
            result["interval_days"],
            result["ease_factor"],
            result["last_reviewed"],
            result["next_due"]

        ))

        conn.commit()

        return result

    finally:

        cursor.close()
        release_connection(conn)