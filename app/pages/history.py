"""Attempt history page - view, filter, and manage past evaluations."""

from __future__ import annotations

import streamlit as st

from app.state.session import SessionStateManager


def render_history_page(session: SessionStateManager):
    """Render the attempt history page."""
    st.markdown('<p class="page-header">Attempt History</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">View and manage your past evaluation attempts</p>', unsafe_allow_html=True)

    from app.services.history_service import HistoryService
    svc = HistoryService()

    total = svc.get_total_count()
    st.markdown(f"**Total Evaluations:** {total}")

    if total == 0:
        st.info("📂 No evaluation history yet. Complete your first evaluation to see it here.")
        return

    # Filters
    col_filter, col_sort = st.columns([2, 1])
    with col_filter:
        from core.enums import Subject
        subjects = ["All Subjects"] + [s.value for s in Subject.ordered_list()]
        selected_subject = st.selectbox("Filter by Subject", subjects, key="history_subject_filter")
    with col_sort:
        st.markdown("")  # Spacing

    # Fetch data
    subject_filter = "" if selected_subject == "All Subjects" else selected_subject
    attempts = svc.get_filtered_attempts(subject=subject_filter, limit=50)

    if not attempts:
        st.info(f"No attempts found for {selected_subject}.")
        return

    # Display as table
    st.markdown("---")

    for i, attempt in enumerate(attempts):
        col1, col2, col3, col4, col5 = st.columns([2, 2, 1.5, 1.5, 1])

        with col1:
            date = attempt.get("created_at", "N/A")
            if len(date) > 10:
                date = date[:10]
            st.markdown(f"**{date}**")

        with col2:
            st.markdown(attempt.get("subject", "N/A"))

        with col3:
            pct = attempt.get("percentage", 0)
            awarded = attempt.get("total_awarded", 0)
            possible = attempt.get("total_possible", 0)
            color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 50 else "#ef4444"
            st.markdown(f'<span style="color:{color}; font-weight:600;">{awarded}/{possible} ({pct:.0f}%)</span>', unsafe_allow_html=True)

        with col4:
            strictness = attempt.get("strictness", 6)
            st.markdown(f"Strictness: {strictness}/10")

        with col5:
            if st.button("🗑️", key=f"del_{i}", help="Delete this attempt"):
                paper_id = attempt.get("paper_id", "")
                if paper_id:
                    svc.delete_attempt(paper_id)
                    st.rerun()

        if i < len(attempts) - 1:
            st.markdown("<hr style='margin:4px 0; border:none; border-top:1px solid #f0f0f0;'>", unsafe_allow_html=True)

    # Pagination hint
    if len(attempts) >= 50:
        st.caption("Showing last 50 attempts. Older attempts are still stored.")
