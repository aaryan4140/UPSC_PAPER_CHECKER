"""Extraction prompt - instructs Gemini to extract questions and answers from PDF."""

EXTRACTION_PROMPT = """You are an expert at reading handwritten UPSC Mains answer sheets.

Analyze this PDF document carefully. It contains a handwritten answer sheet from a UPSC Mains exam candidate.

Your task:
1. Identify each question (look for question numbers like Q1, Q.1, 1., Question 1, etc.)
2. Extract the question text as written
3. Determine the marks allocation (look for patterns like "(10 Marks)", "[15 marks]", "10M", etc. If not visible, estimate based on answer length: short=10, medium=15, long=20)
4. Extract the full handwritten answer text for each question as accurately as possible

Rules:
- Preserve the candidate's original text even if it has grammatical errors
- If handwriting is partially illegible, make your best interpretation and include it
- Number questions sequentially if numbering is unclear
- Include ALL text the candidate wrote for each answer

Respond ONLY with valid JSON in this exact format:
{{
    "questions": [
        {{
            "number": 1,
            "text": "the question text as written",
            "max_marks": 10,
            "answer_text": "the full candidate answer text extracted from handwriting"
        }}
    ],
    "total_questions_found": 3,
    "legibility_notes": "any notes about handwriting quality"
}}"""
