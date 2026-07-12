"""Evaluation result domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class RubricScore:
    """Score for a single rubric component."""

    component: str
    score: float
    max_score: float
    weight: float
    feedback: str = ""

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight

    @property
    def percentage(self) -> float:
        return (self.score / self.max_score * 100) if self.max_score > 0 else 0.0


@dataclass
class QuestionEvaluation:
    """Complete evaluation result for a single question."""

    question_number: int
    max_marks: int
    awarded_marks: float = 0.0
    model_answer: str = ""
    evaluation_text: str = ""
    missing_content: list[str] = field(default_factory=list)
    improvement_suggestions: list[str] = field(default_factory=list)
    upsc_style_feedback: str = ""
    rubric_scores: list[RubricScore] = field(default_factory=list)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)

    @property
    def score_display(self) -> str:
        return f"{self.awarded_marks}/{self.max_marks}"

    @property
    def percentage(self) -> float:
        return (self.awarded_marks / self.max_marks * 100) if self.max_marks > 0 else 0.0


@dataclass
class EvaluationResult:
    """Complete evaluation result for an entire paper."""

    paper_id: str
    question_evaluations: list[QuestionEvaluation] = field(default_factory=list)
    total_marks_awarded: float = 0.0
    total_marks_possible: int = 0
    overall_feedback: str = ""
    evaluated_at: datetime = field(default_factory=datetime.now)
    strictness_used: int = 6
    evaluation_duration_seconds: float = 0.0

    @property
    def total_score_display(self) -> str:
        return f"{self.total_marks_awarded}/{self.total_marks_possible}"

    @property
    def overall_percentage(self) -> float:
        if self.total_marks_possible == 0:
            return 0.0
        return self.total_marks_awarded / self.total_marks_possible * 100

    def compute_totals(self) -> None:
        """Recompute total marks from individual question evaluations."""
        self.total_marks_awarded = sum(qe.awarded_marks for qe in self.question_evaluations)
        self.total_marks_possible = sum(qe.max_marks for qe in self.question_evaluations)
