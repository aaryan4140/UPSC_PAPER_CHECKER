"""Application-wide constants."""

# Supported marks allocations in UPSC
VALID_MARKS = [5, 10, 15, 20, 25, 30, 40, 50, 125, 250]

# Default rubric weights (will be dynamically adjusted by marks)
DEFAULT_RUBRIC_WEIGHTS = {
    "knowledge": 0.25,
    "structure": 0.15,
    "analysis": 0.20,
    "examples": 0.15,
    "presentation": 0.10,
    "current_affairs": 0.05,
    "conclusion": 0.10,
}

# Rubric weight adjustments by marks tier
RUBRIC_WEIGHT_PROFILES = {
    5: {
        "knowledge": 0.35,
        "structure": 0.15,
        "analysis": 0.15,
        "examples": 0.15,
        "presentation": 0.10,
        "current_affairs": 0.00,
        "conclusion": 0.10,
    },
    10: {
        "knowledge": 0.25,
        "structure": 0.15,
        "analysis": 0.20,
        "examples": 0.15,
        "presentation": 0.10,
        "current_affairs": 0.05,
        "conclusion": 0.10,
    },
    15: {
        "knowledge": 0.20,
        "structure": 0.15,
        "analysis": 0.25,
        "examples": 0.15,
        "presentation": 0.10,
        "current_affairs": 0.05,
        "conclusion": 0.10,
    },
    20: {
        "knowledge": 0.20,
        "structure": 0.15,
        "analysis": 0.20,
        "examples": 0.15,
        "presentation": 0.10,
        "current_affairs": 0.10,
        "conclusion": 0.10,
    },
}

# Strictness multipliers applied to scoring
STRICTNESS_MULTIPLIERS = {
    1: 1.20,   # Beginner friendly - generous
    2: 1.15,
    3: 1.10,
    4: 1.05,
    5: 1.02,
    6: 1.00,   # Moderate - baseline
    7: 0.97,
    8: 0.94,   # Strict
    9: 0.90,   # Real UPSC examiner
    10: 0.85,  # UPSC topper level
}

# Maximum file size for uploaded PDFs (in MB)
MAX_PDF_SIZE_MB = 50

# Supported PDF page limit
MAX_PDF_PAGES = 100

# OCR confidence categories
OCR_HIGH_CONFIDENCE = 0.85
OCR_MEDIUM_CONFIDENCE = 0.60
OCR_LOW_CONFIDENCE = 0.40

# App metadata
APP_TITLE = "UPSC Answer Evaluator"
APP_ICON = "📝"
APP_DESCRIPTION = "AI-powered UPSC answer sheet evaluation with detailed feedback"
