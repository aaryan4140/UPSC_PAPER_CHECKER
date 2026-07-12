"""Request schemas for the evaluation pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from core.enums import Subject, StrictnessLevel


@dataclass
class UploadRequest:
    """Schema for PDF upload request."""

    file_bytes: bytes = b""
    filename: str = ""
    subject: Optional[Subject] = None
    strictness: StrictnessLevel = StrictnessLevel.MODERATE

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.file_bytes:
            errors.append("No file data provided.")
        if not self.filename.lower().endswith(".pdf"):
            errors.append("Only PDF files are supported.")
        return errors


@dataclass
class EvaluationRequest:
    """Schema for triggering evaluation on an uploaded paper."""

    paper_id: str = ""
    subject: Optional[Subject] = None
    strictness: StrictnessLevel = StrictnessLevel.MODERATE
    generate_model_answer: bool = True
    include_feedback: bool = True
    include_improvement_suggestions: bool = True
