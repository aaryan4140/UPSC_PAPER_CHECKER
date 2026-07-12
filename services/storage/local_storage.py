"""Local filesystem storage implementation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from core.config import StorageConfig
from core.exceptions import StorageException
from core.logging_config import get_logger
from services.storage.interface import StorageInterface

logger = get_logger(__name__)


class LocalStorage(StorageInterface):
    """Local filesystem-based storage for development and single-user deployment."""

    def __init__(self, config: StorageConfig):
        self._base_path = config.base_path
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create necessary storage directories."""
        (self._base_path / "evaluations").mkdir(parents=True, exist_ok=True)
        (self._base_path / "uploads").mkdir(parents=True, exist_ok=True)
        (self._base_path / "history").mkdir(parents=True, exist_ok=True)

    def save(self, key: str, data: Any) -> str:
        """Save JSON-serializable data to a file."""
        file_path = self._base_path / f"{key}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved data: {key}")
            return key
        except (OSError, TypeError) as e:
            raise StorageException(f"Failed to save data for key: {key}", details={"error": str(e)})

    def load(self, key: str) -> Optional[Any]:
        """Load JSON data from a file."""
        file_path = self._base_path / f"{key}.json"
        if not file_path.exists():
            return None
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise StorageException(f"Failed to load data for key: {key}", details={"error": str(e)})

    def delete(self, key: str) -> bool:
        """Delete a stored file."""
        file_path = self._base_path / f"{key}.json"
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted: {key}")
            return True
        return False

    def list_keys(self, prefix: str = "") -> list[str]:
        """List all stored keys matching prefix."""
        keys = []
        for path in self._base_path.rglob("*.json"):
            key = str(path.relative_to(self._base_path)).replace(".json", "")
            if not prefix or key.startswith(prefix):
                keys.append(key)
        return sorted(keys)

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return (self._base_path / f"{key}.json").exists()

    def save_file(self, file_bytes: bytes, filename: str) -> Path:
        """Save an uploaded file to the uploads directory."""
        upload_path = self._base_path / "uploads" / filename
        upload_path.parent.mkdir(parents=True, exist_ok=True)
        upload_path.write_bytes(file_bytes)
        logger.info(f"Saved upload: {filename} ({len(file_bytes)} bytes)")
        return upload_path
