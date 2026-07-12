"""Text utility functions."""

from __future__ import annotations

import re


def truncate_text(text: str, max_length: int = 500, suffix: str = "...") -> str:
    """Truncate text to a maximum length with suffix."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def clean_ocr_text(text: str) -> str:
    """Clean OCR output text by removing artifacts and normalizing whitespace."""
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    return text


def count_words(text: str) -> int:
    """Count words in text."""
    return len(text.split()) if text.strip() else 0


def highlight_low_confidence(text: str, low_confidence_words: list[str]) -> str:
    """Wrap low-confidence words with HTML highlight tags for UI display."""
    for word in low_confidence_words:
        text = text.replace(
            word,
            f'<span style="background-color: #ffeb3b; padding: 0 2px;">{word}</span>',
        )
    return text
