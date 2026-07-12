"""Validation utility functions."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from core.constants import MAX_PDF_SIZE_MB, VALID_MARKS


def validate_pdf_upload(file_bytes: bytes, filename: str) -> list[str]:
    """Validate an uploaded PDF file. Returns list of error messages."""
    errors: list[str] = []

    if not file_bytes:
        errors.append("No file data received.")
        return errors

    if not filename.lower().endswith(".pdf"):
        errors.append("Only PDF files are accepted.")

    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_PDF_SIZE_MB:
        errors.append(f"File size ({size_mb:.1f} MB) exceeds limit of {MAX_PDF_SIZE_MB} MB.")

    if len(file_bytes) < 100:
        errors.append("File appears to be empty or corrupted.")

    return errors


def validate_marks(marks: int) -> bool:
    """Validate that marks value is reasonable for UPSC."""
    return marks > 0 and marks <= 250
