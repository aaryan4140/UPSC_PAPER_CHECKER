"""Sidebar component with subject selection and configuration."""

from __future__ import annotations

import streamlit as st

from app.state.session import SessionStateManager
from core.enums import Subject, StrictnessLevel
from core.constants import APP_TITLE


def render_sidebar(session: SessionStateManager) -> None:
    """Render the application sidebar with configuration options."""
    with st.sidebar:
        st.markdown(f"### {APP_TITLE}")
        st.markdown("---")

        # Subject selection
        st.markdown("**Subject**")
        subjects = Subject.ordered_list()
        subject_names = [s.value for s in subjects]
        current_subject = session.get("selected_subject")
        default_index = 0
        if current_subject and current_subject in subject_names:
            default_index = subject_names.index(current_subject)

        selected = st.selectbox(
            "Select Subject",
            options=subject_names,
            index=default_index,
            label_visibility="collapsed",
        )
        session.set("selected_subject", selected)

        st.markdown("---")

        # Strictness slider
        st.markdown("**Evaluation Strictness**")
        strictness_value = st.slider(
            "Strictness Level",
            min_value=1,
            max_value=10,
            value=session.get("strictness", 6),
            label_visibility="collapsed",
        )
        strictness_level = StrictnessLevel(strictness_value)
        st.caption(f"Mode: {strictness_level.label}")
        session.set("strictness", strictness_value)

        st.markdown("---")

        # Navigation
        st.markdown("**Navigation**")
        if st.button("Upload Paper", use_container_width=True):
            session.set_current_tab("upload")
            st.rerun()
        if st.button("Evaluation Results", use_container_width=True):
            session.set_current_tab("evaluation")
            st.rerun()
        if st.button("Analytics", use_container_width=True):
            session.set_current_tab("analytics")
            st.rerun()

        st.markdown("---")
        st.caption("UPSC Answer Evaluator v1.0.0")
