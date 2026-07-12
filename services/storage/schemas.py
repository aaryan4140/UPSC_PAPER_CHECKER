"""Storage schemas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class StoredEvaluation:
    """Schema for a persisted evaluation record."""

    key: str = ""
    paper_id: str = ""
    subject: str = ""
    total_score: str = ""
    stored_at: datetime = None
    data_path: str = ""
