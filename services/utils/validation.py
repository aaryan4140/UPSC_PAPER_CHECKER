"""Input validation for the evaluation pipeline."""

from __future__ import annotations

from typing import Any

from core.constants import MAX_PDF_SIZE_MB
from core.exceptions import AppException
from core.logging_config import get_logger

logger = get_logger(__name__)


class ValidationError(AppException):
    """Raised when input validation fails."""
    pass


def validate_pdf_bytes(file_bytes: bytes, filename: str) -> list[str]:
    """Validate uploaded PDF file bytes. Returns list of errors (empty = valid)."""
    errors: list[str] = []

    if not file_bytes:
        errors.append("No file data received.")
        return errors

    if not filename.lower().endswith(".pdf"):
        errors.append("Only PDF files are accepted.")

    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_PDF_SIZE_MB:
        errors.append(f"File size ({size_mb:.1f} MB) exceeds limit of {MAX_PDF_SIZE_MB} MB.")

    # PDF magic bytes check
    if file_bytes[:4] != b"%PDF":
        errors.append("File does not appear to be a valid PDF (invalid header).")

    return errors


def validate_gemini_response(data: Any, required_keys: list[str]) -> list[str]:
    """Validate that a Gemini JSON response contains required keys."""
    if not isinstance(data, dict):
        return [f"Expected dict response, got {type(data).__name__}"]

    missing = [k for k in required_keys if k not in data]
    return [f"Missing required key: {k}" for k in missing]


def validate_score(score: float, max_score: float) -> float:
    """Clamp score to valid range [0, max_score]."""
    if score < 0:
        logger.warning(f"Score {score} below 0, clamping to 0")
        return 0.0
    if score > max_score:
        logger.warning(f"Score {score} exceeds max {max_score}, clamping")
        return max_score
    return score


def validate_marks(marks: int) -> bool:
    """Validate marks value is reasonable for UPSC."""
    return 1 <= marks <= 250


def validate_strictness(strictness: int) -> int:
    """Clamp strictness to valid range [1, 10]."""
    return max(1, min(10, strictness))


def sanitize_text(text: str, max_length: int = 50000) -> str:
    """Sanitize text input by truncating and stripping."""
    if not text:
        return ""
    return text[:max_length].strip()
