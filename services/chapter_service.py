from services.db import (
    get_connection,
    release_connection
)


# ==================================================
# CHAPTERS
# ==================================================

def get_chapters():
    """
    Returns all chapters ordered by chapter number.
    """

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
# CHAPTER SUMMARY
# ==================================================

def get_chapter_summary(chapter_id):
    """
    Returns chapter title and summary.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT
                chapter_title,
                summary_content
            FROM chapters
            WHERE id = %s
        """, (chapter_id,))

        row = cursor.fetchone()

        return row

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# CHAPTER COUNT
# ==================================================

def get_total_chapters():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM chapters
        """)

        total = cursor.fetchone()[0]

        return total

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# BOOK COUNT
# ==================================================

def get_total_books():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM books
        """)

        total = cursor.fetchone()[0]

        return total

    finally:

        cursor.close()
        release_connection(conn)