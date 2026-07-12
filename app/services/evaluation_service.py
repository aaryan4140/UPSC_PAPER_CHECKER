"""Evaluation service - orchestrates the 2-call evaluation pipeline for the UI."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional, Callable

from core.config import get_settings
from core.enums import Subject, StrictnessLevel, EvaluationStatus
from core.logging_config import get_logger
from ai.llm.gemini_client import GeminiClient
from evaluation.evaluator import PaperEvaluator
from models.evaluation_result import EvaluationResult
from models.paper import Paper
from processing.pdf.processor import PDFProcessor

logger = get_logger(__name__)


@dataclass
class EvaluationOutput:
    """Complete output from evaluation for UI consumption."""

    paper: Optional[Paper] = None
    evaluation_result: Optional[EvaluationResult] = None
    status: EvaluationStatus = EvaluationStatus.PENDING
    error_message: str = ""
    processing_time: float = 0.0


class EvaluationService:
    """Service layer for evaluation - called by Streamlit pages."""

    def __init__(self):
        self._settings = get_settings()
        self._pdf_processor = PDFProcessor()
        self._gemini = GeminiClient(self._settings.gemini)
        self._evaluator = PaperEvaluator(self._gemini)

    def evaluate(
        self,
        file_bytes: bytes,
        filename: str,
        subject: Subject,
        strictness: StrictnessLevel,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ) -> EvaluationOutput:
        """Run the 2-call evaluation pipeline with progress updates."""
        output = EvaluationOutput()
        start_time = time.time()

        try:
            # Step 1: Save and validate PDF
            self._update_progress(progress_callback, "Validating PDF...", 0.05)
            file_path = self._pdf_processor.save_uploaded_file(file_bytes, filename)
            metadata = self._pdf_processor.validate_pdf(file_path)

            if not metadata.is_valid:
                output.status = EvaluationStatus.FAILED
                output.error_message = metadata.error_message
                return output

            # Step 2: Extract questions via Gemini Vision (Call 1)
            self._update_progress(progress_callback, "Reading answer sheet (AI extraction)...", 0.15)
            pdf_bytes = file_path.read_bytes()

            # Step 3: Evaluate via Gemini (Calls 2-4, consensus)
            self._update_progress(progress_callback, "Evaluating answers (run 1/3)...", 0.35)
            evaluation_result, paper = self._evaluator.run(
                pdf_bytes=pdf_bytes,
                subject=subject,
                strictness=strictness,
                paper_id=filename,
                progress_callback=progress_callback,
            )

            paper.filename = filename
            paper.page_count = metadata.page_count
            output.paper = paper
            output.evaluation_result = evaluation_result
            output.status = EvaluationStatus.COMPLETED

            # Cleanup temp file
            file_path.unlink(missing_ok=True)

        except Exception as e:
            output.status = EvaluationStatus.FAILED
            output.error_message = str(e)
            logger.error(f"Evaluation failed: {e}", exc_info=True)

        output.processing_time = time.time() - start_time
        self._update_progress(progress_callback, "Complete!", 1.0)
        return output

    def validate_api_key(self) -> bool:
        """Check if Gemini API key is configured."""
        return bool(self._settings.gemini.api_key)

    def _update_progress(self, callback: Optional[Callable], message: str, progress: float) -> None:
        if callback:
            callback(message, progress)
