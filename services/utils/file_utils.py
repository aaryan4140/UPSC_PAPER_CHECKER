"""File utility functions."""

from __future__ import annotations

import tempfile
from pathlib import Path


def save_temp_file(file_bytes: bytes, suffix: str = ".pdf") -> Path:
    """Save bytes to a temporary file and return the path."""
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp.write(file_bytes)
    temp.close()
    return Path(temp.name)


def get_file_size_mb(file_path: Path) -> float:
    """Get file size in megabytes."""
    if not file_path.exists():
        return 0.0
    return file_path.stat().st_size / (1024 * 1024)


def ensure_directory(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return path
