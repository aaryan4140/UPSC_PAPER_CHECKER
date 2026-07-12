"""History service - manages evaluation history for the UI."""

from __future__ import annotations

from pathlib import Path

from core.config import get_settings
from core.logging_config import get_logger
from services.storage.sqlite_storage import SQLiteStorage

logger = get_logger(__name__)


class HistoryService:
    """Manages evaluation history operations."""

    def __init__(self):
        settings = get_settings()
        db_path = settings.storage.base_path / "evaluations.db"
        self._storage = SQLiteStorage(db_path)

    def get_all_attempts(self, limit: int = 100) -> list[dict]:
        """Get all attempts with details."""
        return self._storage.get_attempt_history(limit=limit)

    def get_filtered_attempts(self, subject: str = "", limit: int = 50) -> list[dict]:
        """Get attempts filtered by subject."""
        return self._storage.get_attempt_history(subject=subject, limit=limit)

    def get_evaluation_detail(self, evaluation_id: str) -> dict | None:
        """Get detailed evaluation data."""
        return self._storage.load(evaluation_id)

    def delete_attempt(self, evaluation_id: str) -> bool:
        """Delete an evaluation record."""
        return self._storage.delete(evaluation_id)

    def get_total_count(self) -> int:
        """Get total number of stored evaluations."""
        return self._storage.get_evaluation_count()

    def save_evaluation(self, evaluation_data: dict) -> str:
        """Save evaluation result."""
        return self._storage.save_evaluation(evaluation_data)

    def save_attempt(self, attempt_data: dict) -> None:
        """Save attempt record for analytics."""
        self._storage.save_attempt(attempt_data)
