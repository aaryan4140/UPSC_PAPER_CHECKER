"""Report data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ReportSection:
    """A section within the evaluation report."""

    title: str = ""
    content: str = ""
    section_type: str = "text"  # text, table, chart, comparison
    order: int = 0


@dataclass
class ReportMetadata:
    """Metadata for a generated report."""

    paper_id: str = ""
    generated_at: datetime = field(default_factory=datetime.now)
    format: str = "html"
    subject: str = ""
    total_score: str = ""
    question_count: int = 0
