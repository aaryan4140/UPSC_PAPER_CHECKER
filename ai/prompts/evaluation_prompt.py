"""Evaluation prompt - instructs Gemini to evaluate all answers in a single call."""

from core.constants import DEFAULT_RUBRIC_WEIGHTS, RUBRIC_WEIGHT_PROFILES, STRICTNESS_MULTIPLIERS

STRICTNESS_INSTRUCTIONS = {
    1: "Be very lenient. Accept basic understanding. Reward attempt and effort.",
    2: "Be lenient. Accept reasonable attempts even if incomplete.",
    3: "Be somewhat lenient. Minor gaps are acceptable.",
    4: "Be slightly below moderate. Overlook small issues.",
    5: "Moderate-easy. Expect decent coverage but don't penalize minor gaps.",
    6: "Moderate. Standard UPSC evaluation. Balanced assessment.",
    7: "Above moderate. Expect good coverage and analysis.",
    8: "Strict. Expect comprehensive coverage, strong analysis, good examples.",
    9: "Very strict. Evaluate as a real UPSC examiner. Penalize every gap.",
    10: "Extremely strict. UPSC topper standard. Only award marks for excellence.",
}

SCORING_BANDS = """
MANDATORY SCORING CRITERIA — You MUST follow these bands strictly:

  0-1/10: Completely irrelevant, no meaningful content related to the question
  2-3/10: Minimal attempt. Major factual errors OR only 1-2 vague points. Missing most key concepts.
  4-5/10: Below average. Some relevant points but superficial. Lacks depth, examples, or analysis. Key gaps present.
  6-7/10: Average to good. Covers main points with some analysis. Has a few examples. Minor gaps. Decent structure.
  8-9/10: Very good. Comprehensive coverage, strong analysis, relevant examples/data, clear structure, good conclusion.
  10/10: Exceptional. UPSC topper quality — flawless content, multi-dimensional analysis, precise examples, perfect structure.

RULES:
- A score of 6 means "average" — most candidates who attempt the question properly fall here.
- Only give 8+ if the answer has concrete examples, data, or case studies with analysis.
- Only give 9+ if the answer is near-perfect with zero gaps.
- A blank or irrelevant answer MUST get 0-1.
- Be CONSISTENT: if two answers have similar depth, they MUST get similar scores.
"""


def build_evaluation_prompt(
    extracted_questions: list[dict],
    subject: str,
    strictness: int,
) -> str:
    """Build the comprehensive evaluation prompt for all questions."""
    strictness_instruction = STRICTNESS_INSTRUCTIONS.get(strictness, STRICTNESS_INSTRUCTIONS[6])
    multiplier = STRICTNESS_MULTIPLIERS.get(strictness, 1.0)

    questions_block = ""
    for q in extracted_questions:
        marks = q.get("max_marks", 10)
        weights = RUBRIC_WEIGHT_PROFILES.get(marks, DEFAULT_RUBRIC_WEIGHTS)
        weights_str = ", ".join(f"{k}={v}" for k, v in weights.items())

        questions_block += f"""
---
Question {q['number']} ({marks} marks):
"{q['text']}"

Candidate's Answer:
\"\"\"{q['answer_text']}\"\"\"

Rubric weights for {marks}-mark question: {weights_str}
"""

    return f"""You are a senior UPSC Mains examiner with 20+ years of experience.

**Subject:** {subject}
**Strictness Level:** {strictness}/10 — {strictness_instruction}
**Strictness Multiplier:** {multiplier} (apply to scoring — lower multiplier = stricter)

{SCORING_BANDS}

Evaluate ALL the following questions from a UPSC Mains answer sheet.

For EACH question, provide:
1. **Rubric Scores** — Score each of the 7 components out of 10 using the scoring bands above:
   - knowledge: Factual accuracy, depth of content, key concepts covered
   - analysis: Critical thinking, logical reasoning, multi-dimensional analysis
   - structure: Organization, introduction-body-conclusion flow, paragraph coherence
   - examples: Relevant examples, case studies, data, facts used
   - presentation: Language quality, clarity, grammar, word economy
   - current_affairs: Integration of recent developments, government schemes, reports
   - conclusion: Way forward, balanced conclusion, policy suggestions

2. **Model Answer** — Write an ideal UPSC-quality answer (appropriate length for marks)
3. **Missing Content** — Key concepts, articles, schemes, examples the candidate missed
4. **Improvement Suggestions** — Specific actionable advice to score higher
5. **UPSC Feedback** — One paragraph in the style of a UPSC examiner's margin note
6. **Strengths & Weaknesses** — 3-4 bullet points each
7. **Final Marks** — Calculate as: sum(component_score × weight) × max_marks / 10, then apply multiplier {multiplier}

{questions_block}

Respond ONLY with valid JSON in this EXACT format:
{{
    "evaluations": [
        {{
            "question_number": 1,
            "max_marks": 10,
            "awarded_marks": 6.5,
            "evaluation_text": "Brief overall assessment of the answer",
            "model_answer": "The ideal answer text...",
            "rubric_scores": [
                {{"component": "knowledge", "score": 7.0, "max_score": 10, "weight": 0.25, "feedback": "Good coverage of..."}},
                {{"component": "analysis", "score": 6.0, "max_score": 10, "weight": 0.20, "feedback": "Needs deeper..."}},
                {{"component": "structure", "score": 7.5, "max_score": 10, "weight": 0.15, "feedback": "Well organized..."}},
                {{"component": "examples", "score": 5.0, "max_score": 10, "weight": 0.15, "feedback": "Limited examples..."}},
                {{"component": "presentation", "score": 8.0, "max_score": 10, "weight": 0.10, "feedback": "Clear language..."}},
                {{"component": "current_affairs", "score": 4.0, "max_score": 10, "weight": 0.05, "feedback": "No recent..."}},
                {{"component": "conclusion", "score": 6.0, "max_score": 10, "weight": 0.10, "feedback": "Needs way forward..."}}
            ],
            "missing_content": ["Article 21 interpretation", "Kesavananda Bharati case", "Recent judicial reforms 2024"],
            "improvement_suggestions": ["Add constitutional articles with exact text", "Include a diagram of judicial hierarchy", "Mention recent NJAC judgment"],
            "upsc_style_feedback": "The answer demonstrates basic understanding but lacks the analytical depth expected at this level...",
            "strengths": ["Good introduction", "Correct basic facts", "Legible structure"],
            "weaknesses": ["No case laws cited", "Missing conclusion", "Superficial analysis"]
        }}
    ]
}}

IMPORTANT:
- Evaluate EVERY question listed above
- Keep awarded_marks within 0 to max_marks
- awarded_marks MUST equal the weighted sum: sum(score_i × weight_i) × max_marks / 10 × {multiplier}
- Rubric weights MUST match those specified for each question's marks tier
- Model answer should be {subject}-specific and UPSC-appropriate
- Be consistent with strictness level {strictness}/10 across all questions
- Follow the scoring bands EXACTLY — do not deviate"""
