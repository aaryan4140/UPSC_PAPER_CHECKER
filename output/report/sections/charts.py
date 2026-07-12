"""Charts section for visual score representation."""

from __future__ import annotations

from models.evaluation_result import EvaluationResult


class ChartsSection:
    """Generates chart visualizations for evaluation reports."""

    def render_score_chart(self, result: EvaluationResult) -> str:
        """Render a score distribution chart."""
        # TODO: Phase 4 - Implement chart rendering (plotly or matplotlib)
        raise NotImplementedError("Chart rendering will be implemented in Phase 4.")

    def render_rubric_radar(self, rubric_scores: dict) -> str:
        """Render a radar chart of rubric component scores."""
        # TODO: Phase 4 - Implement radar chart for rubric visualization
        raise NotImplementedError("Radar chart will be implemented in Phase 4.")
