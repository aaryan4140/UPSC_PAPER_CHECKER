"""Attempt history tracking."""

from __future__ import annotations

from typing import Optional

from core.enums import Subject
from core.logging_config import get_logger

logger = get_logger(__name__)


class AttemptHistory:
    """Manages storage and retrieval of evaluation attempt history."""

    def save_attempt(self, evaluation_data: dict) -> str:
        """Save an evaluation attempt to history."""
        # TODO: Phase 4 - Implement attempt persistence
        raise NotImplementedError("Attempt saving will be implemented in Phase 4.")

    def get_all_attempts(self, subject: Optional[Subject] = None) -> list[dict]:
        """Retrieve all attempts, optionally filtered by subject."""
        # TODO: Phase 4 - Implement attempt retrieval
        raise NotImplementedError("Attempt retrieval will be implemented in Phase 4.")

    def get_attempt_count(self) -> int:
        """Get total number of stored attempts."""
        # TODO: Phase 4 - Implement count
        return 0
