"""Common reusable UI components."""

from __future__ import annotations

import streamlit as st


def render_score_card(title: str, score: str, subtitle: str = "") -> None:
    """Render a styled score card."""
    st.markdown(
        f"""
        <div class="score-card">
            <h3 style="margin:0; color:white;">{title}</h3>
            <h1 style="margin:0.5rem 0; color:white;">{score}</h1>
            <p style="margin:0; opacity:0.8;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, description: str = "") -> None:
    """Render a metric card with label and value."""
    st.markdown(
        f"""
        <div class="metric-card">
            <p style="margin:0; font-size:0.8rem; color:#666;">{label}</p>
            <h3 style="margin:0.2rem 0;">{value}</h3>
            <p style="margin:0; font-size:0.75rem; color:#999;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_error(message: str) -> None:
    """Render an error message."""
    st.error(message)


def render_success(message: str) -> None:
    """Render a success message."""
    st.success(message)


def render_info(message: str) -> None:
    """Render an informational message."""
    st.info(message)


def render_processing_spinner(message: str = "Processing..."):
    """Return a spinner context manager."""
    return st.spinner(message)
