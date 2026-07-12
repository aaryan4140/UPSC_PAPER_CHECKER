"""Subject-level analytics and performance breakdown."""

from __future__ import annotations

from core.enums import Subject
from core.logging_config import get_logger

logger = get_logger(__name__)


class SubjectAnalytics:
    """Provides subject-level performance analytics."""

    def get_subject_averages(self) -> dict[str, float]:
        """Get average scores per subject."""
        # TODO: Phase 4 - Implement subject average calculation
        raise NotImplementedError("Subject averages will be implemented in Phase 4.")

    def get_weakest_subject(self) -> str:
        """Identify the subject with lowest average score."""
        # TODO: Phase 4 - Implement weakest subject identification
        raise NotImplementedError("Weakest subject identification will be implemented in Phase 4.")

    def get_strongest_subject(self) -> str:
        """Identify the subject with highest average score."""
        # TODO: Phase 4 - Implement strongest subject identification
        raise NotImplementedError("Strongest subject identification will be implemented in Phase 4.")

    def get_component_breakdown_by_subject(self, subject: Subject) -> dict[str, float]:
        """Get rubric component averages for a specific subject."""
        # TODO: Phase 4 - Implement per-subject component breakdown
        raise NotImplementedError("Component breakdown will be implemented in Phase 4.")
