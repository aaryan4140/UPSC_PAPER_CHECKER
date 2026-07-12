"""Answer domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OCRWord:
    """A single word extracted via OCR with confidence metadata."""

    text: str
    confidence: float
    bounding_box: Optional[list[tuple[float, float]]] = None

    @property
    def is_low_confidence(self) -> bool:
        return self.confidence < 0.6


@dataclass
class Answer:
    """Represents a candidate's handwritten answer extracted from the PDF."""

    question_number: int
    text: str
    raw_ocr_words: list[OCRWord] = field(default_factory=list)
    page_numbers: list[int] = field(default_factory=list)
    word_count: int = 0
    ocr_confidence_mean: float = 0.0
    low_confidence_segments: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.text and not self.word_count:
            self.word_count = len(self.text.split())
        if self.raw_ocr_words and not self.ocr_confidence_mean:
            confidences = [w.confidence for w in self.raw_ocr_words]
            self.ocr_confidence_mean = sum(confidences) / len(confidences) if confidences else 0.0
        if self.raw_ocr_words and not self.low_confidence_segments:
            self.low_confidence_segments = [w.text for w in self.raw_ocr_words if w.is_low_confidence]

    @property
    def has_low_confidence_text(self) -> bool:
        return len(self.low_confidence_segments) > 0
