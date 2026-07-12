"""Abstract interface for storage backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional


class StorageInterface(ABC):
    """Base interface for storage engine implementations."""

    @abstractmethod
    def save(self, key: str, data: Any) -> str:
        """Save data and return a reference key."""
        ...

    @abstractmethod
    def load(self, key: str) -> Optional[Any]:
        """Load data by reference key."""
        ...

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete data by reference key."""
        ...

    @abstractmethod
    def list_keys(self, prefix: str = "") -> list[str]:
        """List all keys, optionally filtered by prefix."""
        ...

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if a key exists in storage."""
        ...

    def save_file(self, file_bytes: bytes, filename: str) -> Path:
        """Save a raw file (PDF, image, etc.)."""
        raise NotImplementedError("File storage not supported by this backend.")
