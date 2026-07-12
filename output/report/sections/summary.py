"""Summary section for reports."""

from __future__ import annotations

from models.evaluation_result import EvaluationResult


class SummarySection:
    """Generates the summary section of evaluation reports."""

    def render(self, result: EvaluationResult) -> str:
        """Render summary section as HTML."""
        # TODO: Phase 4 - Implement summary section rendering
        raise NotImplementedError("Summary section will be implemented in Phase 4.")
