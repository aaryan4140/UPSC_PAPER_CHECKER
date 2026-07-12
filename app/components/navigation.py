"""Navigation component for tab-based routing."""

from __future__ import annotations

import streamlit as st

from app.state.session import SessionStateManager


def render_navigation(session: SessionStateManager) -> None:
    """Render top-level tab navigation."""
    tabs = st.tabs(["Upload", "Evaluation", "Analytics"])

    with tabs[0]:
        if st.button("Go to Upload", key="nav_upload"):
            session.set_current_tab("upload")
            st.rerun()

    with tabs[1]:
        if st.button("Go to Evaluation", key="nav_eval"):
            session.set_current_tab("evaluation")
            st.rerun()

    with tabs[2]:
        if st.button("Go to Analytics", key="nav_analytics"):
            session.set_current_tab("analytics")
            st.rerun()
