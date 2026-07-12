"""Application-wide enumerations."""

from enum import Enum


class Subject(str, Enum):
    """UPSC subjects with pinned ordering."""

    # Pinned subjects (always appear first in UI)
    POLITY = "Polity"
    ECONOMICS = "Economics"
    GEOGRAPHY = "Geography"
    HISTORY = "History"

    # GS Papers
    ETHICS = "Ethics"
    ENVIRONMENT = "Environment"
    SCIENCE_TECH = "Science & Technology"
    INTERNAL_SECURITY = "Internal Security"
    INTERNATIONAL_RELATIONS = "International Relations"
    SOCIAL_JUSTICE = "Social Justice"
    GOVERNANCE = "Governance"
    DISASTER_MANAGEMENT = "Disaster Management"

    # Essay
    ESSAY = "Essay"

    # Optional Subjects
    ANTHROPOLOGY = "Anthropology"
    COMMERCE = "Commerce & Accountancy"
    CIVIL_ENGINEERING = "Civil Engineering"
    ECONOMICS_OPTIONAL = "Economics (Optional)"
    ELECTRICAL_ENGINEERING = "Electrical Engineering"
    GEOGRAPHY_OPTIONAL = "Geography (Optional)"
    GEOLOGY = "Geology"
    HISTORY_OPTIONAL = "History (Optional)"
    LAW = "Law"
    MANAGEMENT = "Management"
    MATHEMATICS = "Mathematics"
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    MEDICAL_SCIENCE = "Medical Science"
    PHILOSOPHY = "Philosophy"
    PHYSICS = "Physics"
    POLITICAL_SCIENCE = "Political Science & IR"
    PSYCHOLOGY = "Psychology"
    PUBLIC_ADMINISTRATION = "Public Administration"
    SOCIOLOGY = "Sociology"
    STATISTICS = "Statistics"
    ZOOLOGY = "Zoology"
    BOTANY = "Botany"
    CHEMISTRY = "Chemistry"
    LITERATURE = "Literature"
    AGRICULTURE = "Agriculture"

    @classmethod
    def pinned(cls) -> list["Subject"]:
        """Return the four pinned subjects."""
        return [cls.POLITY, cls.ECONOMICS, cls.GEOGRAPHY, cls.HISTORY]

    @classmethod
    def ordered_list(cls) -> list["Subject"]:
        """Return all subjects with pinned ones first."""
        pinned = cls.pinned()
        remaining = [s for s in cls if s not in pinned]
        return pinned + remaining


class StrictnessLevel(int, Enum):
    """Evaluation strictness scale."""

    BEGINNER_FRIENDLY = 1
    EASY = 2
    LENIENT = 3
    BELOW_MODERATE = 4
    MODERATE_EASY = 5
    MODERATE = 6
    ABOVE_MODERATE = 7
    STRICT = 8
    REAL_UPSC_EXAMINER = 9
    UPSC_TOPPER_LEVEL = 10

    @property
    def label(self) -> str:
        labels = {
            1: "Beginner Friendly",
            2: "Easy",
            3: "Lenient",
            4: "Below Moderate",
            5: "Moderate Easy",
            6: "Moderate",
            7: "Above Moderate",
            8: "Strict",
            9: "Real UPSC Examiner",
            10: "UPSC Topper Level",
        }
        return labels[self.value]


class EvaluationStatus(str, Enum):
    """Status of an evaluation task."""

    PENDING = "pending"
    PROCESSING = "processing"
    OCR_COMPLETE = "ocr_complete"
    EXTRACTING = "extracting"
    EVALUATING = "evaluating"
    COMPLETED = "completed"
    FAILED = "failed"


class OCRProvider(str, Enum):
    """Supported OCR providers."""

    PADDLE_OCR = "paddleocr"
    EASY_OCR = "easyocr"
    GOOGLE_VISION = "google_vision"
    AZURE_OCR = "azure_ocr"


class LLMProvider(str, Enum):
    """Supported LLM providers."""

    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


class ReportFormat(str, Enum):
    """Supported report output formats."""

    HTML = "html"
    PDF = "pdf"
    JSON = "json"
    MARKDOWN = "markdown"


class RubricComponent(str, Enum):
    """Evaluation rubric components."""

    KNOWLEDGE = "knowledge"
    STRUCTURE = "structure"
    ANALYSIS = "analysis"
    EXAMPLES = "examples"
    PRESENTATION = "presentation"
    CURRENT_AFFAIRS = "current_affairs"
    CONCLUSION = "conclusion"


class PaperType(str, Enum):
    """UPSC paper types."""

    GS1 = "General Studies Paper 1"
    GS2 = "General Studies Paper 2"
    GS3 = "General Studies Paper 3"
    GS4 = "General Studies Paper 4 (Ethics)"
    ESSAY = "Essay"
    OPTIONAL = "Optional Subject"


class Directive(str, Enum):
    """UPSC question directives."""

    DISCUSS = "Discuss"
    CRITICALLY_EXAMINE = "Critically Examine"
    ANALYSE = "Analyse"
    EVALUATE = "Evaluate"
    COMMENT = "Comment"
    EXPLAIN = "Explain"
    ENUMERATE = "Enumerate"
    COMPARE = "Compare and Contrast"
    JUSTIFY = "Justify"
    ILLUSTRATE = "Illustrate"
    ELUCIDATE = "Elucidate"
    EXAMINE = "Examine"
    DIFFERENTIATE = "Differentiate"
    ASSESS = "Assess"
    REVIEW = "Review"
    INFER = "Infer"
    INTERPRET = "Interpret"


class Difficulty(str, Enum):
    """Question difficulty levels."""

    EASY = "Easy"
    MODERATE = "Moderate"
    HARD = "Hard"
    VERY_HARD = "Very Hard"


class MissingContentPriority(str, Enum):
    """Priority levels for missing content items."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
