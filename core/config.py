"""Application configuration loaded exclusively from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class GeminiConfig:
    """Gemini API configuration."""

    api_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    model_name: str = field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-2.0-flash"))
    temperature: float = field(default_factory=lambda: float(os.getenv("GEMINI_TEMPERATURE", "0.3")))
    max_output_tokens: int = field(default_factory=lambda: int(os.getenv("GEMINI_MAX_TOKENS", "32768")))
    timeout: int = field(default_factory=lambda: int(os.getenv("GEMINI_TIMEOUT", "300")))
    max_retries: int = field(default_factory=lambda: int(os.getenv("GEMINI_MAX_RETRIES", "5")))


@dataclass(frozen=True)
class StorageConfig:
    """Storage configuration."""

    engine: str = field(default_factory=lambda: os.getenv("STORAGE_ENGINE", "local"))
    base_path: Path = field(default_factory=lambda: Path(os.getenv("STORAGE_PATH", str(BASE_DIR / "data"))))


@dataclass(frozen=True)
class AppConfig:
    """General application configuration."""

    app_name: str = "UPSC Answer Evaluator"
    version: str = "1.0.0"
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_dir: Path = field(default_factory=lambda: BASE_DIR / "logs")


@dataclass(frozen=True)
class Settings:
    """Root settings container aggregating all configuration sections."""

    app: AppConfig = field(default_factory=AppConfig)
    gemini: GeminiConfig = field(default_factory=GeminiConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)

    def validate(self) -> list[str]:
        """Return list of configuration warnings/errors."""
        issues: list[str] = []
        if not self.gemini.api_key:
            issues.append("GEMINI_API_KEY is not set in environment.")
        return issues


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Singleton settings accessor."""
    return Settings()
