"""Individual question report section."""

from __future__ import annotations

from models.evaluation_result import QuestionEvaluation


class QuestionReportSection:
    """Generates per-question sections in the report."""

    def render(self, evaluation: QuestionEvaluation) -> str:
        """Render a single question's evaluation as HTML."""
        # TODO: Phase 4 - Implement per-question report section
        raise NotImplementedError("Question report section will be implemented in Phase 4.")
