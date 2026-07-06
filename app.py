import streamlit as st

from services.chapter_service import (
    get_chapters,
    get_chapter_summary
)

from services.summary_parser import (
    extract_subtopics
)

from services.session import (
    require_login
)

# ==================================================
# LOGIN
# ==================================================

require_login()

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Learning OS",
    layout="wide"
)

st.title("📚 Learning OS")

# ==================================================
# LOAD CHAPTERS
# ==================================================

chapters = get_chapters()

if not chapters:

    st.warning("No chapters found.")

    st.stop()

chapter_map = {
    title: chapter_id
    for chapter_id, title in chapters
}

selected_title = st.selectbox(
    "Select Chapter",
    options=list(chapter_map.keys())
)

chapter_id = chapter_map[selected_title]

# ==================================================
# LOAD SUMMARY
# ==================================================

chapter = get_chapter_summary(
    chapter_id
)

if chapter is None:

    st.error("Chapter not found.")

    st.stop()

chapter_title, summary_content = chapter

# ==================================================
# HEADER
# ==================================================

st.divider()

st.header(chapter_title)

# ==================================================
# SUMMARY STATS
# ==================================================

word_count = len(
    summary_content.split()
)

subtopics = extract_subtopics(
    summary_content
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Subtopics",
        len(subtopics)
    )

with col2:

    st.metric(
        "Summary Words",
        word_count
    )

st.divider()

# ==================================================
# QUICK NAVIGATION
# ==================================================

if subtopics:

    st.subheader(
        "📑 Subtopics"
    )

    for topic in subtopics:

        st.markdown(
            f"- {topic['title']}"
        )

    st.divider()

# ==================================================
# SUBTOPIC VIEW
# ==================================================

for index, topic in enumerate(
    subtopics,
    start=1
):

    with st.expander(
        f"{index}. {topic['title']}",
        expanded=False
    ):

        st.markdown(
            topic["content"]
        )

# ==================================================
# FALLBACK
# ==================================================

if len(subtopics) == 0:

    st.markdown(
        summary_content
    )