"""Question domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from core.enums import Directive, Subject


@dataclass
class Question:
    """Represents a single UPSC question extracted from the answer sheet."""

    number: int
    text: str
    max_marks: int
    directive: Optional[Directive] = None
    subject: Optional[Subject] = None
    sub_parts: list["Question"] = field(default_factory=list)
    page_number: int = 0
    raw_text: str = ""

    @property
    def has_sub_parts(self) -> bool:
        return len(self.sub_parts) > 0

    @property
    def total_marks(self) -> int:
        if self.has_sub_parts:
            return sum(part.max_marks for part in self.sub_parts)
        return self.max_marks

    def __repr__(self) -> str:
        return f"Question(number={self.number}, marks={self.max_marks}, directive={self.directive})"
