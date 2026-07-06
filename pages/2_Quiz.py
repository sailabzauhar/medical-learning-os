
import streamlit as st

from services.srs_service import (
    get_learning_mcq,
    get_subtopics
)

from services.srs_update import update_srs

from services.high_yield_service import (
    get_high_yield_points
)

from services.session import (
    require_login,
    get_user_id
)

from services.quiz_service import (
    get_chapters,
    get_progress,
    save_answer,
    reset_chapter
)

require_login()


CURRENT_USER_ID = get_user_id()


# ==================================================
# DATABASE
# ==================================================



# ==================================================
# CHAPTERS
# ==================================================



# ==================================================
# PROGRESS
# ==================================================


# ==================================================
# SAVE ATTEMPT
# ==================================================


# ==================================================
# RESET
# ==================================================



# ==================================================
# SESSION
# ==================================================

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

if "current_mcq_id" not in st.session_state:
    st.session_state.current_mcq_id = None


# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="Subtopic SM2 Quiz + High Yield",
    layout="wide"
)

st.title("🧠 Learning OS")

st.caption(
    "Subtopic Learning + SM-2 + High-Yield Revision"
)

# ==================================================
# CHAPTER
# ==================================================

chapters = get_chapters()

chapter_map = {
    title: cid
    for cid, title in chapters
}

selected_title = st.selectbox(
    "Select Chapter",
    list(chapter_map.keys())
)

chapter_id = chapter_map[selected_title]

# ==================================================
# SUBTOPIC
# ==================================================

subtopics = get_subtopics(chapter_id)

subtopic_options = ["All Subtopics"]

for section, count in subtopics:

    subtopic_options.append(
        f"{section} ({count} MCQs)"
    )

selected_subtopic = st.selectbox(
    "Select Subtopic",
    subtopic_options
)

source_filter = None

if selected_subtopic != "All Subtopics":

    source_filter = selected_subtopic.rsplit(
        " (",
        1
    )[0]

# ==================================================
# PROGRESS
# ==================================================

completed, total = get_progress(
    chapter_id,
    CURRENT_USER_ID
)
progress = 0

if total > 0:
    progress = completed / total

st.progress(progress)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Introduced",
        completed
    )

with col2:
    st.metric(
        "Total MCQs",
        total
    )

with col3:

    if st.button(
        "🔄 Reset Chapter"
    ):

        reset_chapter(
            chapter_id,
            CURRENT_USER_ID
        )

        st.session_state.submitted = False
        st.session_state.selected_answer = None
        st.session_state.current_mcq_id = None

        st.rerun()

# ==================================================
# FETCH MCQ
# ==================================================

mcq, mode = get_learning_mcq(
    chapter_id,
    CURRENT_USER_ID,
    source_filter
)

if mcq is None:

    st.success(
        "🎉 No questions available for this subtopic."
    )

    st.stop()

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
    source_section,
    difficulty
) = mcq

# ==================================================
# RESET SESSION
# ==================================================

if st.session_state.current_mcq_id != mcq_id:

    st.session_state.current_mcq_id = mcq_id
    st.session_state.submitted = False
    st.session_state.selected_answer = None

# ==================================================
# MODE BADGE
# ==================================================

st.divider()

if mode == "review":
    st.warning(
        "🔁 Due Review"
    )

if mode == "new":
    st.info(
        "🆕 New Question"
    )

st.subheader(
    source_section
)

if difficulty:

    st.caption(
        f"Difficulty: {difficulty}"
    )

# ==================================================
# QUESTION
# ==================================================

st.markdown(question)

selected = st.radio(
    "Choose Answer",
    ["A", "B", "C", "D"],
    format_func=lambda x: {
        "A": f"A. {option_a}",
        "B": f"B. {option_b}",
        "C": f"C. {option_c}",
        "D": f"D. {option_d}"
    }[x],
    key=f"answer_{mcq_id}"
)

# ==================================================
# SUBMIT
# ==================================================

if not st.session_state.submitted:

    if st.button(
        "Submit Answer"
    ):

        st.session_state.submitted = True
        st.session_state.selected_answer = selected

        st.rerun()

# ==================================================
# RESULT
# ==================================================

if st.session_state.submitted:

    selected = (
        st.session_state.selected_answer
    )

    correct = (
        selected == correct_answer
    )

    if correct:

        st.success(
            "✅ Correct"
        )

    else:

        st.error(
            f"❌ Incorrect. Correct Answer: {correct_answer}"
        )

    # ----------------------------------------------
    # EXPLANATION
    # ----------------------------------------------

    st.markdown(
        "## 📖 Explanation"
    )

    st.write(
        correct_reason
    )

    # ----------------------------------------------
    # KEY LEARNING
    # ----------------------------------------------

    st.markdown(
        "## 🎯 Key Learning Point"
    )

    st.info(
        key_learning_point
    )

    # ----------------------------------------------
    # HIGH YIELD
    # ----------------------------------------------

    points = get_high_yield_points(
        chapter_id,
        source_section
    )


    if points:

        st.markdown(
            "## ⚡ High-Yield Revision"
        )

        for point in points:

            st.info(point)

    else:

        st.error(
            "No High-Yield Points Found"
        )

    # ----------------------------------------------
    # MEMORY RATING
    # ----------------------------------------------

    default_quality = (
        4 if correct else 2
    )

    quality_labels = {
        5: "5 - Perfect recall",
        4: "4 - Correct after hesitation",
        3: "3 - Correct with difficulty",
        2: "2 - Incorrect but familiar",
        1: "1 - Remembered after seeing answer",
        0: "0 - Complete blackout"
    }

    st.markdown(
        "## 🧠 Memory Rating"
    )

    quality = st.selectbox(
        "Adjust only if needed",
        options=[5, 4, 3, 2, 1, 0],
        index=[5, 4, 3, 2, 1, 0].index(
            default_quality
        ),
        format_func=lambda x:
        quality_labels[x]
    )

    # ----------------------------------------------
    # NEXT
    # ----------------------------------------------

    if st.button(
        "Next Question ➜"
    ):

        save_answer(
            CURRENT_USER_ID,
            mcq_id,
            selected,
            correct_answer
        )

        update_srs(
            CURRENT_USER_ID,
            mcq_id,
            quality
        )

        st.session_state.submitted = False
        st.session_state.selected_answer = None
        st.session_state.current_mcq_id = None

        st.rerun()