"""Paper domain model representing a complete uploaded answer sheet."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

from core.enums import Subject, PaperType, EvaluationStatus
from models.question import Question
from models.answer import Answer


@dataclass
class Paper:
    """Represents a complete UPSC answer sheet uploaded by the candidate."""

    id: str = field(default_factory=lambda: str(uuid4()))
    filename: str = ""
    subject: Optional[Subject] = None
    paper_type: Optional[PaperType] = None
    questions: list[Question] = field(default_factory=list)
    answers: list[Answer] = field(default_factory=list)
    total_marks: int = 0
    status: EvaluationStatus = EvaluationStatus.PENDING
    uploaded_at: datetime = field(default_factory=datetime.now)
    evaluated_at: Optional[datetime] = None
    page_count: int = 0

    @property
    def question_count(self) -> int:
        return len(self.questions)

    @property
    def max_possible_marks(self) -> int:
        return sum(q.max_marks for q in self.questions)

    def get_answer_for_question(self, question_number: int) -> Optional[Answer]:
        """Retrieve the answer corresponding to a question number."""
        for answer in self.answers:
            if answer.question_number == question_number:
                return answer
        return None
