# Developer Guide

## Module Reference

### Core (`core/`)
Central configuration and shared infrastructure.

| File | Responsibility |
|------|---------------|
| `config.py` | Loads all settings from `.env` via dataclasses |
| `enums.py` | Subject, Directive, Difficulty, Strictness, etc. |
| `constants.py` | Rubric weights, strictness multipliers, limits |
| `exceptions.py` | Exception hierarchy (OCR, LLM, Evaluation, Storage) |
| `logging_config.py` | Rotating file + console logging setup |

### OCR (`ocr/`)
Pluggable OCR with provider interface pattern.

- **Interface**: `OCRProviderInterface` — implement `process_pdf()`, `process_image()`
- **Manager**: `OCRManager` — registers providers, delegates processing
- **Schemas**: `OCRResult` → `OCRPageResult` → `OCRLineResult` → `OCRWordResult`
- **Adding a provider**: Create class in `ocr/providers/`, implement interface, register in pipeline

### Extraction (`extraction/`)
Parses raw OCR text into structured questions and answers.

- `QuestionParser` — regex-based multi-format question detection
- `AnswerExtractor` — boundary detection between questions
- `MarksExtractor` — detects marks allocation patterns

### LLM (`llm/`)
Provider-agnostic LLM client layer.

- `LLMProviderInterface` — abstract base for any LLM
- `GeminiClient` — production Gemini client using `google.genai` SDK
- `RetryHandler` — exponential backoff for transient failures
- `RateLimiter` — token-bucket rate limiting

### Prompts (`prompts/`)
Centralized prompt management with versioning.

- `registry.py` — `PromptRegistry` with version tracking
- `manager.py` — `PromptManager` constructs prompts from templates
- `templates/` — 15+ individual prompt files, each returning JSON

### Evaluation (`evaluation/`)
The core evaluation engine.

- `EvaluationEngine` — orchestrates full pipeline
- `DirectiveDetector` — identifies 17 UPSC directives
- `SubjectDetector` — keyword-based subject validation
- `DifficultyDetector` — multi-factor difficulty assessment
- `ModelAnswerGenerator` — generates ideal answers via LLM
- `FeedbackGenerator` — missing content + improvements + examiner feedback
- `FinalJudge` — holistic scoring with strictness adjustment

### Rubric (`rubric/`)
Dynamic rubric generation and component evaluation.

- `RubricGenerator` — creates rubrics with weights by marks tier
- `components/` — 7 evaluators (Knowledge, Analysis, Structure, Presentation, Examples, Current Affairs, Conclusion)

### Scoring (`scoring/`)
Score calculation without normalization.

- `ScoringEngine` — applies strictness multipliers
- `ScoreAggregator` — sums individual question scores (no normalization to 100)

### Storage (`storage/`)
Pluggable persistence layer.

- `StorageInterface` — abstract base
- `LocalStorage` — JSON file-based storage
- `SQLiteStorage` — production storage with schema migrations

### App (`app/`)
Streamlit frontend with service layer pattern.

- **Pages**: evaluation, analytics, history, settings
- **Services**: EvaluationService, AnalyticsService, ReportService, HistoryService, ConfigurationService
- **Pattern**: UI → Service → Backend (never direct backend access from pages)

## Extension Points

### Adding an OCR Provider
1. Create `ocr/providers/your_provider.py`
2. Implement `OCRProviderInterface`
3. Register in `services/pipeline.py` or `EvaluationService`

### Adding an LLM Provider
1. Create `llm/your_client.py`
2. Implement `LLMProviderInterface`
3. Swap in `EvaluationEngine.__init__()`

### Adding a Rubric Component
1. Create `rubric/components/your_component.py`
2. Add to `core/constants.py` weight profiles
3. Add evaluator call in `EvaluationEngine._run_component_evaluations()`

### Adding a Prompt
1. Create `prompts/templates/your_prompt.py`
2. Add method to `PromptManager`
3. Register in `PromptRegistry`

## Code Conventions

- **Type hints** on all function signatures
- **Dataclasses** for structured data (not dicts)
- **Logging** via `get_logger(__name__)` — never `print()`
- **Exceptions** from `core/exceptions.py` hierarchy
- **Configuration** only from `.env` via `get_settings()`
- **No hardcoded strings** — use constants/enums
- **Single responsibility** — one class, one job
