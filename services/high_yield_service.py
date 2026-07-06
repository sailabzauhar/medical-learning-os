import re

from services.db import (
    get_connection,
    release_connection
)


# ==================================================
# GET CHAPTER SUMMARY
# ==================================================

def get_summary(chapter_id):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT summary_content
            FROM chapters
            WHERE id = %s
        """, (chapter_id,))

        row = cursor.fetchone()

        if row:
            return row[0]

        return ""

    finally:

        cursor.close()
        release_connection(conn)


# ==================================================
# TEXT NORMALIZATION
# ==================================================

def clean_text(text):

    text = text.upper()

    text = re.sub(
        r"\(.*?\)",
        "",
        text
    )

    text = re.sub(
        r"[^A-Z0-9 ]",
        " ",
        text
    )

    text = " ".join(
        text.split()
    )

    return text


# ==================================================
# EXTRACT SUBTOPICS
# ==================================================

def extract_subtopics(summary):

    return re.findall(
        r"^##\s+(.*?)$",
        summary,
        flags=re.MULTILINE
    )


# ==================================================
# FIND BEST MATCH
# ==================================================

def find_best_heading(
    source_section,
    headings
):

    source_words = set(
        clean_text(source_section).split()
    )

    best_heading = None
    best_score = -1

    for heading in headings:

        heading_words = set(
            clean_text(heading).split()
        )

        score = len(
            source_words.intersection(
                heading_words
            )
        )

        if score > best_score:

            best_score = score
            best_heading = heading

    return best_heading


# ==================================================
# HIGH-YIELD EXTRACTION
# ==================================================

def get_high_yield_points(
    chapter_id,
    source_section
):

    summary = get_summary(
        chapter_id
    )

    if not summary:
        return []

    headings = extract_subtopics(
        summary
    )

    if not headings:
        return []

    matched_heading = find_best_heading(
        source_section,
        headings
    )

    if not matched_heading:
        return []

    pattern = (
        rf"##\s+{re.escape(matched_heading)}"
        rf"(.*?)(?=\n##\s+|\Z)"
    )

    match = re.search(
        pattern,
        summary,
        re.DOTALL | re.IGNORECASE
    )

    if not match:
        return []

    section_text = match.group(1)

    hy_pattern = (
        r"###\s+High-Yield Revision Points"
        r"(.*?)(?=\n###\s+|\Z)"
    )

    hy_match = re.search(
        hy_pattern,
        section_text,
        re.DOTALL | re.IGNORECASE
    )

    if not hy_match:
        return []

    high_yield_text = hy_match.group(1)

    points = []

    for line in high_yield_text.splitlines():

        line = line.strip()

        if line.startswith(("-", "•", "*")):

            point = (
                line.replace("-", "")
                .replace("•", "")
                .replace("*", "")
                .strip()
            )

            if point:
                points.append(point)

    return points