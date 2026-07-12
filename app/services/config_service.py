"""Configuration service - manages application settings."""

from __future__ import annotations

import os
from pathlib import Path

from core.config import get_settings
from core.logging_config import get_logger

logger = get_logger(__name__)


class ConfigurationService:
    """Manages runtime application configuration."""

    def get_current_config(self) -> dict:
        """Get current application configuration for display."""
        settings = get_settings()
        return {
            "gemini_model": settings.gemini.model_name,
            "gemini_temperature": settings.gemini.temperature,
            "gemini_max_tokens": settings.gemini.max_output_tokens,
            "ocr_provider": settings.ocr.provider,
            "ocr_confidence_threshold": settings.ocr.confidence_threshold,
            "ocr_language": settings.ocr.language,
            "storage_engine": settings.storage.engine,
            "log_level": settings.app.log_level,
            "debug": settings.app.debug,
            "api_key_configured": bool(settings.gemini.api_key),
        }

    def validate_configuration(self) -> list[str]:
        """Validate current configuration and return issues."""
        settings = get_settings()
        return settings.validate()

    def get_available_models(self) -> list[str]:
        """List available Gemini models."""
        return [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash",
        ]

    def get_available_ocr_providers(self) -> list[str]:
        """List available OCR providers."""
        return ["paddleocr", "easyocr", "google_vision", "azure_ocr"]
