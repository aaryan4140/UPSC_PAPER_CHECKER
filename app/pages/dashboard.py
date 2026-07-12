"""Dashboard page - combines Evaluation and History as sub-tabs."""

from __future__ import annotations

import streamlit as st

from app.state.session import SessionStateManager


def render_dashboard_page(session: SessionStateManager):
    """Render the dashboard with subject/strictness selectors and sub-tabs."""
    # Subject & Strictness selectors - always visible at top
    from core.enums import Subject, StrictnessLevel

    col_subj, col_strict, col_mode = st.columns([2, 2, 1])

    with col_subj:
        subjects = Subject.ordered_list()
        subject_names = [s.value for s in subjects]
        current_subject = session.get("selected_subject", "Polity")
        idx = subject_names.index(current_subject) if current_subject in subject_names else 0
        selected_subject = st.selectbox("📚 Subject", subject_names, index=idx, key="dash_subject")
        session.set("selected_subject", selected_subject)

    with col_strict:
        strictness = st.slider(
            "🎚️ Strictness Level", min_value=1, max_value=10,
            value=session.get("strictness", 6), key="dash_strictness",
        )
        session.set("strictness", strictness)

    with col_mode:
        level = StrictnessLevel(strictness)
        st.markdown(f"""
        <div style="margin-top: 1.6rem; text-align: center; padding: 8px 12px;
             background: rgba(21, 101, 192, 0.15); border-radius: 10px;
             border: 1px solid rgba(21, 101, 192, 0.3);">
            <span style="color: #90caf9; font-weight: 700; font-size: 0.85rem;">{level.label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Sub-tabs for Evaluate and History
    tab_evaluate, tab_history = st.tabs(["📝  Evaluate", "📜  History"])

    with tab_evaluate:
        from app.pages.evaluation import render_evaluation_page
        render_evaluation_page(session)

    with tab_history:
        from app.pages.history import render_history_page
        render_history_page(session)
