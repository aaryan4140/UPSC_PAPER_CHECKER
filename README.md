# UPSC Answer Evaluator

AI-powered evaluation tool for UPSC Mains answer sheets. Uses Google Gemini for intelligent extraction and evaluation with consensus scoring, model answer generation, and UPSC examiner-style feedback.

## Features

- **PDF Upload** — Upload handwritten answer sheets; Gemini Vision extracts questions and answers directly
- **3-Run Consensus Scoring** — Evaluates each paper 3 times and takes median scores for consistency
- **Strictness Control** — 10-level scale from lenient to UPSC topper standard
- **Model Answers** — Generates ideal UPSC-quality answers for comparison
- **Missing Content Detection** — Identifies missing concepts, articles, schemes, examples
- **UPSC Examiner Feedback** — Realistic examiner-style assessment with strengths/weaknesses
- **Analytics Dashboard** — Track progress with charts and subject-wise performance
- **History** — View past evaluations stored in SQLite
- **Streamlit UI** — Clean, modern single-page app with tabbed navigation

## Project Structure

```
├── app/                        # Streamlit UI layer
│   ├── main.py                 # App entry point
│   ├── pages/                  # Page implementations
│   │   ├── dashboard.py        # Main dashboard (evaluation + history tabs)
│   │   ├── evaluation.py       # Upload + results
│   │   ├── analytics.py        # Performance charts
│   │   ├── history.py          # Past evaluations
│   │   └── settings.py         # Configuration
│   ├── services/               # Service layer (UI ↔ Backend)
│   ├── components/             # Reusable UI components
│   ├── assets/                 # Images, CSS, templates
│   └── state/                  # Session state management
├── ai/                         # AI/LLM layer
│   ├── llm/                    # Gemini client, retry logic
│   │   ├── gemini_client.py    # HTTP client for Gemini API
│   │   ├── interface.py        # Abstract LLM interface
│   │   └── retry.py            # Retry with exponential backoff
│   └── prompts/                # Prompt definitions
│       ├── evaluation_prompt.py # Scoring prompt with rubric bands
│       └── extraction_prompt.py # PDF extraction prompt
├── core/                       # Configuration, enums, exceptions, logging
├── evaluation/                 # Evaluation engine
│   └── evaluator.py            # PaperEvaluator (extract + 3-run consensus)
├── models/                     # Domain models (Paper, Question, Answer, Results)
├── processing/                 # PDF processing
│   └── pdf/processor.py        # PDF validation and page handling
├── services/                   # Backend services
│   ├── storage/                # SQLite + local filesystem storage
│   └── utils/                  # File, text, validation utilities
├── data/                       # Runtime data storage
├── logs/                       # Application logs
├── requirements.txt            # Python dependencies
└── run.py                      # Application launcher
```

## Quick Start

### Prerequisites

- Python 3.11+
- Gemini API key ([Get one here](https://aistudio.google.com/apikey))
- poppler-utils (for PDF processing): `brew install poppler` (Mac) / `apt install poppler-utils` (Linux)

### Installation

```bash
# Clone the repository
git clone https://github.com/aaryan4140/UPSC_PAPER_CHECKER.git
cd UPSC_PAPER_CHECKER

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env - add your GEMINI_API_KEY
```

### Run

```bash
# Direct launch
streamlit run app/main.py

# Or via runner script
python run.py
```

## How It Works

```
PDF Upload → Gemini Vision Extraction (questions + handwritten answers)
    → 3× Evaluation Runs (with strictness-aware rubric)
    → Median Consensus Scoring
    → For each question:
        - Rubric-based component scores
        - Model answer generation
        - Missing content detection
        - Improvement suggestions
        - UPSC examiner feedback
    → Total Score (SUM of question marks)
    → SQLite Storage → Analytics
```

## Scoring System

- **Consensus:** Each paper is evaluated 3 times; median scores are used for reliability
- **No normalization** — total score = sum of individual question marks
- **Strictness multipliers** (1-10 scale) control scoring leniency
- **Rubric components:** Knowledge, Analysis, Structure, Examples, Presentation, Current Affairs, Conclusion

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GEMINI_API_KEY` | (required) | Google Gemini API key |
| `GEMINI_MODEL` | `gemini-2.0-flash` | Gemini model to use |
| `GEMINI_TEMPERATURE` | `0.3` | Generation temperature |
| `GEMINI_MAX_TOKENS` | `32768` | Max output tokens |
| `GEMINI_TIMEOUT` | `300` | Request timeout (seconds) |
| `GEMINI_MAX_RETRIES` | `5` | Max retry attempts |
| `STORAGE_ENGINE` | `local` | Storage backend |
| `STORAGE_PATH` | `./data` | Data storage directory |
| `LOG_LEVEL` | `INFO` | Logging level |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "GEMINI_API_KEY not set" | Add key to `.env` file |
| PDF processing fails | Install poppler: `brew install poppler` / `apt install poppler-utils` |
| Gemini rate limit | Built-in retry with exponential backoff handles this automatically |
| Slow evaluation | Normal — 3 consensus runs + rate limiting gaps (~30s total) |

## License

Private — All rights reserved.
