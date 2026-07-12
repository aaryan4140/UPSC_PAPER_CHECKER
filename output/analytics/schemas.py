"""Analytics schemas for data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class AttemptRecord:
    """Record of a single evaluation attempt."""

    id: str = ""
    paper_id: str = ""
    subject: str = ""
    total_awarded: float = 0.0
    total_possible: int = 0
    percentage: float = 0.0
    strictness_used: int = 6
    evaluated_at: datetime = field(default_factory=datetime.now)
    question_count: int = 0
    component_scores: dict[str, float] = field(default_factory=dict)


@dataclass
class TrendPoint:
    """Single data point in a trend series."""

    timestamp: datetime = field(default_factory=datetime.now)
    score_percentage: float = 0.0
    subject: str = ""


@dataclass
class PerformanceSummary:
    """Aggregate performance summary."""

    total_attempts: int = 0
    average_percentage: float = 0.0
    best_percentage: float = 0.0
    worst_percentage: float = 0.0
    improvement_trend: str = "stable"  # improving, declining, stable
    weak_areas: list[str] = field(default_factory=list)
    strong_areas: list[str] = field(default_factory=list)
