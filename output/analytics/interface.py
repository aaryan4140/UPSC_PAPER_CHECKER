"""Abstract interface for analytics engines."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.enums import Subject


class AnalyticsInterface(ABC):
    """Base interface for analytics implementations."""

    @abstractmethod
    def get_attempt_history(self, subject: Optional[Subject] = None) -> list[dict]:
        """Retrieve historical attempt data."""
        ...

    @abstractmethod
    def get_average_scores(self, subject: Optional[Subject] = None) -> dict[str, float]:
        """Calculate average scores across attempts."""
        ...

    @abstractmethod
    def get_weak_areas(self) -> list[dict]:
        """Identify consistently weak rubric components."""
        ...

    @abstractmethod
    def get_strong_areas(self) -> list[dict]:
        """Identify consistently strong rubric components."""
        ...

    @abstractmethod
    def get_trend_data(self, subject: Optional[Subject] = None) -> list[dict]:
        """Get score trend data over time."""
        ...
