"""Abstract interface for evaluation engines."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.enums import StrictnessLevel, Subject
from models.evaluation_result import EvaluationResult, QuestionEvaluation
from models.paper import Paper


class EvaluationEngineInterface(ABC):
    """Base interface for evaluation engine implementations."""

    @abstractmethod
    def evaluate_paper(self, paper: Paper, strictness: StrictnessLevel = StrictnessLevel.MODERATE) -> EvaluationResult:
        """Evaluate an entire paper and return aggregated results."""
        ...

    @abstractmethod
    def evaluate_question(
        self,
        question_text: str,
        answer_text: str,
        max_marks: int,
        strictness: StrictnessLevel = StrictnessLevel.MODERATE,
        subject: Optional[Subject] = None,
    ) -> QuestionEvaluation:
        """Evaluate a single question-answer pair."""
        ...

    @abstractmethod
    def generate_model_answer(
        self,
        question_text: str,
        max_marks: int,
        subject: Optional[Subject] = None,
    ) -> str:
        """Generate a model answer for a given question."""
        ...
