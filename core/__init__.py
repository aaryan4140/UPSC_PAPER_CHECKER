"""Core module - Configuration, constants, exceptions, and logging."""

from core.config import Settings, get_settings
from core.exceptions import (
    AppException,
    OCRException,
    LLMException,
    EvaluationException,
    StorageException,
    PDFProcessingException,
)
from core.enums import (
    Subject,
    StrictnessLevel,
    EvaluationStatus,
    OCRProvider,
    LLMProvider,
    ReportFormat,
)

__all__ = [
    "Settings",
    "get_settings",
    "AppException",
    "OCRException",
    "LLMException",
    "EvaluationException",
    "StorageException",
    "PDFProcessingException",
    "Subject",
    "StrictnessLevel",
    "EvaluationStatus",
    "OCRProvider",
    "LLMProvider",
    "ReportFormat",
]
