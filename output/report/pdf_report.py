"""PDF report generator placeholder."""

from __future__ import annotations

from pathlib import Path

from core.logging_config import get_logger
from models.evaluation_result import EvaluationResult
from output.report.interface import ReportGeneratorInterface

logger = get_logger(__name__)


class PDFReportGenerator(ReportGeneratorInterface):
    """Generates PDF evaluation reports for download."""

    def generate_html(self, result: EvaluationResult) -> str:
        """Generate HTML (intermediate step for PDF)."""
        # TODO: Phase 4 - Implement HTML generation for PDF conversion
        raise NotImplementedError("HTML generation for PDF will be implemented in Phase 4.")

    def generate_pdf(self, result: EvaluationResult, output_path: Path) -> Path:
        """Generate downloadable PDF report."""
        # TODO: Phase 4 - Implement PDF generation using weasyprint or reportlab
        raise NotImplementedError("PDF report generation will be implemented in Phase 4.")

    def get_report_sections(self, result: EvaluationResult) -> list[dict]:
        """Get structured sections for PDF layout."""
        # TODO: Phase 4 - Define PDF-specific section layout
        raise NotImplementedError("PDF report sections will be implemented in Phase 4.")
