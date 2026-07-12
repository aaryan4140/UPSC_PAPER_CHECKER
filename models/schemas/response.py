"""Response schemas for evaluation results."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class QuestionResponse:
    """Response schema for a single question evaluation."""

    question_number: int = 0
    question_text: str = ""
    candidate_answer: str = ""
    max_marks: int = 0
    awarded_marks: float = 0.0
    model_answer: str = ""
    evaluation: str = ""
    missing_content: list[str] = field(default_factory=list)
    improvements: list[str] = field(default_factory=list)
    upsc_feedback: str = ""
    rubric_breakdown: dict[str, float] = field(default_factory=dict)


@dataclass
class EvaluationResponse:
    """Response schema for complete paper evaluation."""

    paper_id: str = ""
    status: str = "completed"
    total_marks_awarded: float = 0.0
    total_marks_possible: int = 0
    questions: list[QuestionResponse] = field(default_factory=list)
    overall_feedback: str = ""
    evaluated_at: Optional[datetime] = None
    strictness_used: int = 6
