"""Abstract interface for LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class LLMProviderInterface(ABC):
    """Base interface that all LLM providers must implement."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize the LLM client (API keys, model loading, etc.)."""
        ...

    @abstractmethod
    def generate(self, prompt: str, system_instruction: Optional[str] = None, **kwargs: Any) -> str:
        """Generate a response from the LLM given a prompt."""
        ...

    @abstractmethod
    def generate_structured(self, prompt: str, response_schema: dict, **kwargs: Any) -> dict:
        """Generate a structured (JSON) response from the LLM."""
        ...

    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the name of this LLM provider."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is configured and available."""
        ...

    def get_token_count(self, text: str) -> int:
        """Estimate token count for a text. Override for accurate counting."""
        return len(text.split()) * 2  # Rough estimate
