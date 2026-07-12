"""Retry handler with exponential backoff for LLM API calls."""

from __future__ import annotations

import time
from typing import Callable, TypeVar, Any

from core.exceptions import LLMException, LLMRateLimitException, LLMTimeoutException
from core.logging_config import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


class RetryHandler:
    """Handles retry logic with exponential backoff for transient failures."""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
    ):
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._exponential_base = exponential_base

    def execute_with_retry(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute a function with retry logic on transient failures."""
        last_exception: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                return func(*args, **kwargs)
            except LLMRateLimitException as e:
                last_exception = e
                delay = self._calculate_delay(attempt)
                logger.warning(f"Rate limited (attempt {attempt + 1}/{self._max_retries + 1}). Retrying in {delay:.1f}s")
                time.sleep(delay)
            except LLMTimeoutException as e:
                last_exception = e
                delay = self._calculate_delay(attempt)
                logger.warning(f"Timeout (attempt {attempt + 1}/{self._max_retries + 1}). Retrying in {delay:.1f}s")
                time.sleep(delay)
            except LLMException:
                raise

        raise LLMException(
            f"Failed after {self._max_retries + 1} attempts. Last error: {last_exception}",
            details={"last_error": str(last_exception)},
        )

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay with exponential backoff."""
        delay = self._base_delay * (self._exponential_base ** attempt)
        return min(delay, self._max_delay)
