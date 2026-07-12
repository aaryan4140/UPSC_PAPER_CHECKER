"""Gemini API client - direct HTTP API calls via requests (no SDK)."""

from __future__ import annotations

import base64
import json
import time
from typing import Any, Optional

import requests

from core.config import GeminiConfig
from core.exceptions import LLMException, LLMRateLimitException, LLMTimeoutException
from core.logging_config import get_logger
from ai.llm.interface import LLMProviderInterface
from ai.llm.retry import RetryHandler

logger = get_logger(__name__)

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiClient(LLMProviderInterface):
    """Google Gemini API client using direct HTTP calls (no SDK)."""

    def __init__(self, config: GeminiConfig):
        self._config = config
        self._retry_handler = RetryHandler(max_retries=config.max_retries)
        self._session: Optional[requests.Session] = None
        self._initialized = False

    def initialize(self) -> None:
        """Validate API key and create HTTP session."""
        if not self._config.api_key:
            raise LLMException("Gemini API key is not configured.")
        self._session = requests.Session()
        self._session.headers.update({"Content-Type": "application/json"})
        self._session.trust_env = False
        self._initialized = True
        logger.info(f"Gemini client ready (model: {self._config.model_name})")

    def generate(self, prompt: str, system_instruction: Optional[str] = None, **kwargs: Any) -> str:
        """Generate text response from Gemini via HTTP API."""
        self._ensure_initialized()

        def _call() -> str:
            url = (
                f"{GEMINI_API_BASE}/{self._config.model_name}:generateContent"
                f"?key={self._config.api_key}"
            )

            payload: dict[str, Any] = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": kwargs.get("temperature", self._config.temperature),
                    "maxOutputTokens": kwargs.get("max_tokens", self._config.max_output_tokens),
                },
            }

            if system_instruction:
                payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

            return self._send_request(url, payload)

        return self._retry_handler.execute_with_retry(_call)

    def generate_structured(self, prompt: str, response_schema: dict | None = None, **kwargs: Any) -> dict:
        """Generate structured JSON response from Gemini."""
        system_instruction = kwargs.pop("system_instruction", None)
        json_prompt = prompt + "\n\nRespond ONLY with valid JSON. No markdown, no explanation."
        raw = self.generate(json_prompt, system_instruction=system_instruction, **kwargs)
        return self._parse_json_response(raw)

    def generate_with_pdf(self, pdf_bytes: bytes, prompt: str, system_instruction: Optional[str] = None, **kwargs: Any) -> dict:
        """Send PDF to Gemini multimodal endpoint and get structured JSON response."""
        self._ensure_initialized()

        pdf_b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        json_prompt = prompt + "\n\nRespond ONLY with valid JSON. No markdown, no explanation."

        def _call() -> str:
            url = (
                f"{GEMINI_API_BASE}/{self._config.model_name}:generateContent"
                f"?key={self._config.api_key}"
            )

            payload: dict[str, Any] = {
                "contents": [{
                    "parts": [
                        {"inline_data": {"mime_type": "application/pdf", "data": pdf_b64}},
                        {"text": json_prompt},
                    ]
                }],
                "generationConfig": {
                    "temperature": kwargs.get("temperature", self._config.temperature),
                    "maxOutputTokens": kwargs.get("max_tokens", self._config.max_output_tokens),
                },
            }

            if system_instruction:
                payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

            return self._send_request(url, payload)

        raw = self._retry_handler.execute_with_retry(_call)
        return self._parse_json_response(raw)

    def get_provider_name(self) -> str:
        return "Gemini"

    def is_available(self) -> bool:
        return bool(self._config.api_key)

    @property
    def model_name(self) -> str:
        return self._config.model_name

    def _ensure_initialized(self) -> None:
        if not self._initialized:
            self.initialize()

    def _send_request(self, url: str, payload: dict) -> str:
        """Send request to Gemini API and return text response."""
        start = time.time()
        try:
            resp = self._session.post(url, json=payload, timeout=self._config.timeout)
        except requests.exceptions.Timeout:
            raise LLMTimeoutException("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise LLMTimeoutException(f"Connection error (retryable): {e}")
        except requests.exceptions.RequestException as e:
            raise LLMException(f"Request failed: {e}")

        elapsed = time.time() - start

        if resp.status_code == 429:
            raise LLMRateLimitException(f"Rate limited (429): {resp.text[:200]}")
        if resp.status_code != 200:
            raise LLMException(
                f"Gemini API error (HTTP {resp.status_code}): {resp.text[:300]}",
                details={"status_code": resp.status_code},
            )

        response_data = resp.json()
        logger.info(f"Gemini response in {elapsed:.2f}s")

        text = self._extract_text(response_data)
        if not text:
            raise LLMException("Gemini returned empty response.", details={"response": str(response_data)[:500]})
        return text

    def _extract_text(self, response: dict) -> str:
        """Extract text from Gemini API response JSON."""
        try:
            candidates = response.get("candidates", [])
            if not candidates:
                return ""
            content = candidates[0].get("content", {})
            parts = content.get("parts", [])
            if not parts:
                return ""
            return parts[0].get("text", "")
        except (IndexError, KeyError, TypeError):
            return ""

    def _parse_json_response(self, raw: str) -> dict:
        """Extract and parse JSON from response text."""
        text = raw.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            raise LLMException("Failed to parse JSON from Gemini response.", details={"raw": raw[:500]})
