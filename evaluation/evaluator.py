"""Paper evaluator - Extract + Evaluate with 3-run consensus scoring."""

from __future__ import annotations

import time
from statistics import median
from typing import Optional

from core.enums import Subject, StrictnessLevel
from core.logging_config import get_logger
from ai.llm.gemini_client import GeminiClient
from ai.prompts.extraction_prompt import EXTRACTION_PROMPT
from ai.prompts.evaluation_prompt import build_evaluation_prompt
from models.evaluation_result import EvaluationResult, QuestionEvaluation, RubricScore
from models.paper import Paper
from models.question import Question
from models.answer import Answer

logger = get_logger(__name__)

CONSENSUS_RUNS = 3
RATE_LIMIT_GAP = 8


class PaperEvaluator:
    """Evaluates UPSC answer sheets: 1 extraction call + 3 evaluation calls (median)."""

    def __init__(self, gemini_client: GeminiClient):
        self._client = gemini_client

    def extract_from_pdf(self, pdf_bytes: bytes) -> list[dict]:
        """Call 1: Send PDF to Gemini multimodal, get structured questions+answers."""
        logger.info("Call 1: Extracting questions and answers from PDF via Gemini Vision")

        result = self._client.generate_with_pdf(
            pdf_bytes=pdf_bytes,
            prompt=EXTRACTION_PROMPT,
            system_instruction="You are an expert OCR and document analysis system specialized in reading handwritten exam papers. Always respond in valid JSON.",
        )

        questions = result.get("questions", [])
        logger.info(f"Extraction complete: {len(questions)} questions found")
        return questions

    def evaluate_consensus(
        self,
        extracted_questions: list[dict],
        subject: str,
        strictness: int,
        paper_id: str = "",
        progress_callback=None,
    ) -> EvaluationResult:
        """Run evaluation 3 times and take median scores for consistency."""
        prompt = build_evaluation_prompt(extracted_questions, subject, strictness)
        system_instruction = (
            f"You are a senior UPSC Mains examiner. Strictness: {strictness}/10. "
            "Evaluate with precision and fairness. Always respond in valid JSON."
        )

        results: list[EvaluationResult] = []

        for i in range(CONSENSUS_RUNS):
            logger.info(f"Evaluation run {i + 1}/{CONSENSUS_RUNS}")
            if progress_callback:
                progress_callback(f"Evaluating (run {i + 1}/{CONSENSUS_RUNS})...", 0.50 + (i * 0.15))

            raw = self._client.generate_structured(prompt, system_instruction=system_instruction)
            result = self._parse_evaluation_result(raw, paper_id, strictness)
            results.append(result)

            if i < CONSENSUS_RUNS - 1:
                time.sleep(RATE_LIMIT_GAP)

        return self._compute_median_result(results, paper_id, strictness)

    def run(
        self,
        pdf_bytes: bytes,
        subject: Subject,
        strictness: StrictnessLevel,
        paper_id: str = "",
        progress_callback=None,
    ) -> tuple[EvaluationResult, Paper]:
        """Full flow: Extract then Evaluate×3 with median. Returns (result, paper)."""
        start_time = time.time()
        subject_str = subject.value if subject else "General Studies"
        strictness_val = strictness.value if isinstance(strictness, StrictnessLevel) else strictness

        # Call 1: Extract
        extracted = self.extract_from_pdf(pdf_bytes)

        if not extracted:
            raise ValueError("Could not extract any questions from the PDF.")

        # Build Paper object from extraction
        paper = Paper(id=paper_id, subject=subject)
        for q_data in extracted:
            paper.questions.append(Question(
                number=q_data.get("number", 0),
                text=q_data.get("text", ""),
                max_marks=q_data.get("max_marks", 10),
            ))
            paper.answers.append(Answer(
                question_number=q_data.get("number", 0),
                text=q_data.get("answer_text", ""),
            ))

        # Calls 2-4: Evaluate with consensus
        time.sleep(RATE_LIMIT_GAP)
        result = self.evaluate_consensus(
            extracted, subject_str, strictness_val, paper_id, progress_callback
        )
        result.evaluation_duration_seconds = time.time() - start_time

        logger.info(f"Complete: {result.total_score_display} in {result.evaluation_duration_seconds:.1f}s")
        return result, paper

    def _compute_median_result(
        self,
        results: list[EvaluationResult],
        paper_id: str,
        strictness: int,
    ) -> EvaluationResult:
        """Compute median scores across multiple evaluation runs."""
        if len(results) == 1:
            return results[0]

        # Use the first result as template for structure (model answers, feedback, etc.)
        base = results[0]
        final = EvaluationResult(paper_id=paper_id, strictness_used=strictness)

        num_questions = min(len(r.question_evaluations) for r in results)

        for q_idx in range(num_questions):
            base_qe = base.question_evaluations[q_idx]

            # Median of awarded_marks across runs
            all_marks = [r.question_evaluations[q_idx].awarded_marks for r in results if q_idx < len(r.question_evaluations)]
            median_marks = round(median(all_marks), 1)

            # Median of each rubric component score
            median_rubrics = []
            num_components = len(base_qe.rubric_scores)
            for c_idx in range(num_components):
                all_scores = []
                for r in results:
                    if q_idx < len(r.question_evaluations) and c_idx < len(r.question_evaluations[q_idx].rubric_scores):
                        all_scores.append(r.question_evaluations[q_idx].rubric_scores[c_idx].score)

                if all_scores:
                    base_rs = base_qe.rubric_scores[c_idx]
                    median_rubrics.append(RubricScore(
                        component=base_rs.component,
                        score=round(median(all_scores), 1),
                        max_score=base_rs.max_score,
                        weight=base_rs.weight,
                        feedback=base_rs.feedback,
                    ))

            final.question_evaluations.append(QuestionEvaluation(
                question_number=base_qe.question_number,
                max_marks=base_qe.max_marks,
                awarded_marks=median_marks,
                model_answer=base_qe.model_answer,
                evaluation_text=base_qe.evaluation_text,
                missing_content=base_qe.missing_content,
                improvement_suggestions=base_qe.improvement_suggestions,
                upsc_style_feedback=base_qe.upsc_style_feedback,
                rubric_scores=median_rubrics,
                strengths=base_qe.strengths,
                weaknesses=base_qe.weaknesses,
            ))

        final.compute_totals()
        logger.info(f"Consensus: median marks from {CONSENSUS_RUNS} runs → {final.total_score_display}")
        return final

    def _parse_evaluation_result(
        self,
        raw: dict,
        paper_id: str,
        strictness: int,
    ) -> EvaluationResult:
        """Parse LLM JSON response into EvaluationResult with QuestionEvaluations."""
        result = EvaluationResult(paper_id=paper_id, strictness_used=strictness)

        evaluations = raw.get("evaluations", [])
        for eval_data in evaluations:
            rubric_scores = []
            for rs in eval_data.get("rubric_scores", []):
                rubric_scores.append(RubricScore(
                    component=rs.get("component", ""),
                    score=float(rs.get("score", 0)),
                    max_score=float(rs.get("max_score", 10)),
                    weight=float(rs.get("weight", 0)),
                    feedback=rs.get("feedback", ""),
                ))

            max_marks = int(eval_data.get("max_marks", 10))
            awarded = float(eval_data.get("awarded_marks", 0))
            awarded = max(0.0, min(awarded, float(max_marks)))

            qe = QuestionEvaluation(
                question_number=int(eval_data.get("question_number", 0)),
                max_marks=max_marks,
                awarded_marks=round(awarded, 1),
                model_answer=eval_data.get("model_answer", ""),
                evaluation_text=eval_data.get("evaluation_text", ""),
                missing_content=eval_data.get("missing_content", []),
                improvement_suggestions=eval_data.get("improvement_suggestions", []),
                upsc_style_feedback=eval_data.get("upsc_style_feedback", ""),
                rubric_scores=rubric_scores,
                strengths=eval_data.get("strengths", []),
                weaknesses=eval_data.get("weaknesses", []),
            )
            result.question_evaluations.append(qe)

        result.compute_totals()
        return result
