"""Abstract interface for report generators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from models.evaluation_result import EvaluationResult


class ReportGeneratorInterface(ABC):
    """Base interface for report generation implementations."""

    @abstractmethod
    def generate_html(self, result: EvaluationResult) -> str:
        """Generate an HTML report string."""
        ...

    @abstractmethod
    def generate_pdf(self, result: EvaluationResult, output_path: Path) -> Path:
        """Generate a PDF report file."""
        ...

    @abstractmethod
    def get_report_sections(self, result: EvaluationResult) -> list[dict]:
        """Get structured report sections for rendering."""
        ...
