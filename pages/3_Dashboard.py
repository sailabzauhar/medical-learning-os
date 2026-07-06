import streamlit as st

from services.session import (
    require_login,
    get_user_id
)

from services.dashboard_service import (
    get_dashboard_metrics
)

# ==================================================
# LOGIN
# ==================================================

require_login()

CURRENT_USER_ID = get_user_id()

# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="Learning Dashboard",
    layout="wide"
)

st.title("📊 Learning Dashboard")

metrics = get_dashboard_metrics(
    CURRENT_USER_ID
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Chapters Completed",
        f"{metrics['completed_chapters']}/{metrics['total_chapters']}"
    )

with col2:

    st.metric(
        "Concepts Covered",
        metrics["concepts_covered"]
    )

with col3:

    st.metric(
        "MCQ Accuracy",
        f"{metrics['accuracy']}%"
    )