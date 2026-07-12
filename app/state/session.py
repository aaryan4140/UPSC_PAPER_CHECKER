"""Session state management for Streamlit."""

from __future__ import annotations

import streamlit as st
from typing import Any, Optional

from core.enums import Subject, StrictnessLevel


class SessionStateManager:
    """Manages Streamlit session state with type-safe accessors."""

    DEFAULT_STATE = {
        "current_tab": "upload",
        "selected_subject": "Polity",
        "strictness": StrictnessLevel.ABOVE_MODERATE.value,
        "uploaded_file": None,
        "paper_id": None,
        "evaluation_result": None,
        "ocr_result": None,
        "processing": False,
        "error_message": None,
        "history": [],
    }

    def initialize(self) -> None:
        """Initialize session state with defaults if not already set."""
        for key, default in self.DEFAULT_STATE.items():
            if key not in st.session_state:
                st.session_state[key] = default

    def get_current_tab(self) -> str:
        """Get the currently active tab."""
        return st.session_state.get("current_tab", "upload")

    def set_current_tab(self, tab: str) -> None:
        """Set the active tab."""
        st.session_state["current_tab"] = tab

    def get_subject(self) -> Optional[Subject]:
        """Get the selected subject."""
        value = st.session_state.get("selected_subject")
        if value:
            return Subject(value)
        return None

    def set_subject(self, subject: Optional[Subject]) -> None:
        """Set the selected subject."""
        st.session_state["selected_subject"] = subject.value if subject else None

    def get_strictness(self) -> StrictnessLevel:
        """Get the current strictness level."""
        value = st.session_state.get("strictness", 6)
        return StrictnessLevel(value)

    def set_strictness(self, level: int) -> None:
        """Set the strictness level."""
        st.session_state["strictness"] = level

    def get(self, key: str, default: Any = None) -> Any:
        """Generic getter for session state."""
        return st.session_state.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Generic setter for session state."""
        st.session_state[key] = value

    def is_processing(self) -> bool:
        """Check if evaluation is in progress."""
        return st.session_state.get("processing", False)

    def set_processing(self, state: bool) -> None:
        """Set processing state."""
        st.session_state["processing"] = state

    def set_error(self, message: Optional[str]) -> None:
        """Set or clear error message."""
        st.session_state["error_message"] = message

    def get_error(self) -> Optional[str]:
        """Get current error message."""
        return st.session_state.get("error_message")

    def clear_error(self) -> None:
        """Clear error message."""
        st.session_state["error_message"] = None

    def reset(self) -> None:
        """Reset session state to defaults."""
        for key, default in self.DEFAULT_STATE.items():
            st.session_state[key] = default
