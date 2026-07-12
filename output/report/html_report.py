"""HTML report generator placeholder."""

from __future__ import annotations

from pathlib import Path

from core.logging_config import get_logger
from models.evaluation_result import EvaluationResult
from output.report.interface import ReportGeneratorInterface

logger = get_logger(__name__)


class HTMLReportGenerator(ReportGeneratorInterface):
    """Generates HTML evaluation reports for display in Streamlit."""

    def generate_html(self, result: EvaluationResult) -> str:
        """Generate complete HTML report."""
        # TODO: Phase 4 - Implement HTML report with template engine
        raise NotImplementedError("HTML report generation will be implemented in Phase 4.")

    def generate_pdf(self, result: EvaluationResult, output_path: Path) -> Path:
        """Generate PDF from HTML report."""
        # TODO: Phase 4 - Implement HTML-to-PDF conversion
        raise NotImplementedError("PDF generation will be implemented in Phase 4.")

    def get_report_sections(self, result: EvaluationResult) -> list[dict]:
        """Get structured sections for the report."""
        # TODO: Phase 4 - Define report section structure
        raise NotImplementedError("Report sections will be implemented in Phase 4.")
