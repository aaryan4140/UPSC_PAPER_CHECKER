"""Analytics service - provides data for analytics dashboard."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from core.config import get_settings
from core.logging_config import get_logger
from services.storage.sqlite_storage import SQLiteStorage

logger = get_logger(__name__)


class AnalyticsService:
    """Provides analytics data from stored evaluations."""

    def __init__(self):
        settings = get_settings()
        db_path = settings.storage.base_path / "evaluations.db"
        self._storage = SQLiteStorage(db_path)

    def get_attempt_history(self, subject: str = "", limit: int = 50) -> list[dict]:
        """Get evaluation attempt history."""
        return self._storage.get_attempt_history(subject=subject, limit=limit)

    def get_subject_averages(self) -> dict[str, float]:
        """Get average scores by subject."""
        return self._storage.get_subject_averages()

    def get_total_attempts(self) -> int:
        """Get total number of attempts."""
        return self._storage.get_evaluation_count()

    def get_overall_stats(self) -> dict:
        """Get overall statistics."""
        history = self._storage.get_attempt_history(limit=1000)
        if not history:
            return {"total": 0, "average": 0, "highest": 0, "lowest": 0}

        percentages = [h.get("percentage", 0) for h in history if h.get("percentage")]
        if not percentages:
            return {"total": len(history), "average": 0, "highest": 0, "lowest": 0}

        return {
            "total": len(history),
            "average": round(sum(percentages) / len(percentages), 1),
            "highest": round(max(percentages), 1),
            "lowest": round(min(percentages), 1),
        }

    def get_recent_attempts(self, limit: int = 10) -> list[dict]:
        """Get most recent attempts."""
        return self._storage.get_attempt_history(limit=limit)

    def get_subject_history(self, subject: str) -> list[dict]:
        """Get history for a specific subject."""
        return self._storage.get_attempt_history(subject=subject)
