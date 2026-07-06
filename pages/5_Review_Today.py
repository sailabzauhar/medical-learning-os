import streamlit as st

from services.review_service import (
    get_due_count,
    get_next_due_review
)

from services.quiz_service import (
    save_answer
)

from services.srs_update import (
    update_srs
)

from services.session import (
    require_login,
    get_user_id
)

# ==================================================
# LOGIN
# ==================================================

require_login()

CURRENT_USER_ID = get_user_id()

# ==================================================
# SESSION
# ==================================================

if "review_submitted" not in st.session_state:
    st.session_state.review_submitted = False

if "review_selected" not in st.session_state:
    st.session_state.review_selected = None

if "review_mcq_id" not in st.session_state:
    st.session_state.review_mcq_id = None

# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="Review Today",
    layout="wide"
)

st.title("🔥 Review Today")

# ==================================================
# DUE COUNT
# ==================================================

due_count = get_due_count(
    CURRENT_USER_ID
)

st.metric(
    "Due Reviews",
    due_count
)

if due_count == 0:

    st.success(
        "🎉 No reviews due today."
    )

    st.stop()

# ==================================================
# LOAD REVIEW
# ==================================================

review = get_next_due_review(
    CURRENT_USER_ID
)

if review is None:

    st.success(
        "🎉 No reviews due today."
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
    difficulty,
    chapter_title,
    next_due
) = review

# ==================================================
# RESET SESSION
# ==================================================

if st.session_state.review_mcq_id != mcq_id:

    st.session_state.review_mcq_id = mcq_id
    st.session_state.review_submitted = False
    st.session_state.review_selected = None

# ==================================================
# HEADER
# ==================================================

st.warning(
    f"Review Due Since: {next_due}"
)

st.caption(
    f"{chapter_title} • {source_section}"
)

st.divider()

if difficulty:

    st.caption(
        f"Difficulty: {difficulty}"
    )

# ==================================================
# QUESTION
# ==================================================

st.markdown(question)

selected = st.radio(
    "Choose an answer",
    ["A", "B", "C", "D"],
    format_func=lambda x: {
        "A": f"A. {option_a}",
        "B": f"B. {option_b}",
        "C": f"C. {option_c}",
        "D": f"D. {option_d}"
    }[x],
    key=f"review_answer_{mcq_id}"
)

# ==================================================
# SUBMIT
# ==================================================

if not st.session_state.review_submitted:

    if st.button("Submit Answer"):

        st.session_state.review_submitted = True
        st.session_state.review_selected = selected

        st.rerun()

# ==================================================
# RESULT
# ==================================================

if st.session_state.review_submitted:

    selected = st.session_state.review_selected

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

    st.markdown(
        "## 📖 Explanation"
    )

    st.write(
        correct_reason
    )

    st.markdown(
        "## 🎯 Key Learning Point"
    )

    st.info(
        key_learning_point
    )

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
        options=[5,4,3,2,1,0],
        index=[5,4,3,2,1,0].index(
            default_quality
        ),
        format_func=lambda x:
        quality_labels[x]
    )

    if st.button(
        "Next Review ➜"
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

        st.session_state.review_submitted = False
        st.session_state.review_selected = None
        st.session_state.review_mcq_id = None

        st.rerun()