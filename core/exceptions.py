"""Custom exception hierarchy for the application."""


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class OCRException(AppException):
    """Raised when OCR processing encounters an error."""
    pass


class PDFProcessingException(AppException):
    """Raised when PDF processing fails."""
    pass


class LLMException(AppException):
    """Raised when LLM API call fails."""
    pass


class LLMRateLimitException(LLMException):
    """Raised when LLM rate limit is hit."""
    pass


class LLMTimeoutException(LLMException):
    """Raised when LLM request times out."""
    pass


class EvaluationException(AppException):
    """Raised when evaluation logic encounters an error."""
    pass


class RubricException(AppException):
    """Raised when rubric generation or application fails."""
    pass


class StorageException(AppException):
    """Raised when storage operations fail."""
    pass


class ExtractionException(AppException):
    """Raised when question/answer extraction fails."""
    pass


class ReportException(AppException):
    """Raised when report generation fails."""
    pass


class ConfigurationException(AppException):
    """Raised when configuration is invalid or missing."""
    pass
