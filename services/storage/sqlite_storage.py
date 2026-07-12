"""SQLite storage implementation for evaluation history."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from core.logging_config import get_logger
from services.storage.interface import StorageInterface

logger = get_logger(__name__)


class SQLiteStorage(StorageInterface):
    """SQLite-based storage for evaluation history and analytics."""

    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id TEXT PRIMARY KEY,
                    paper_id TEXT NOT NULL,
                    subject TEXT,
                    strictness INTEGER DEFAULT 6,
                    total_awarded REAL DEFAULT 0,
                    total_possible INTEGER DEFAULT 0,
                    percentage REAL DEFAULT 0,
                    question_count INTEGER DEFAULT 0,
                    evaluation_data TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS question_evaluations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    evaluation_id TEXT NOT NULL,
                    question_number INTEGER,
                    question_text TEXT,
                    answer_text TEXT,
                    max_marks INTEGER,
                    awarded_marks REAL,
                    model_answer TEXT,
                    missing_content TEXT,
                    improvements TEXT,
                    upsc_feedback TEXT,
                    rubric_scores TEXT,
                    strengths TEXT,
                    weaknesses TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (evaluation_id) REFERENCES evaluations(id)
                );

                CREATE TABLE IF NOT EXISTS attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT,
                    subject TEXT,
                    strictness INTEGER,
                    total_awarded REAL,
                    total_possible INTEGER,
                    percentage REAL,
                    component_averages TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_evaluations_subject ON evaluations(subject);
                CREATE INDEX IF NOT EXISTS idx_attempts_subject ON attempts(subject);
                CREATE INDEX IF NOT EXISTS idx_attempts_created ON attempts(created_at);
            """)
        logger.info(f"SQLite database initialized at {self._db_path}")

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        conn = sqlite3.connect(str(self._db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, key: str, data: Any) -> str:
        """Save data as JSON blob."""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO evaluations (id, paper_id, evaluation_data, created_at) VALUES (?, ?, ?, ?)",
                (key, data.get("paper_id", key), json.dumps(data, default=str), datetime.now().isoformat()),
            )
        return key

    def load(self, key: str) -> Optional[Any]:
        """Load data by key."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT evaluation_data FROM evaluations WHERE id = ?", (key,)).fetchone()
            if row:
                return json.loads(row["evaluation_data"])
        return None

    def delete(self, key: str) -> bool:
        """Delete by key."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM evaluations WHERE id = ?", (key,))
            return cursor.rowcount > 0

    def list_keys(self, prefix: str = "") -> list[str]:
        """List all evaluation IDs."""
        with self._get_connection() as conn:
            if prefix:
                rows = conn.execute("SELECT id FROM evaluations WHERE id LIKE ?", (f"{prefix}%",)).fetchall()
            else:
                rows = conn.execute("SELECT id FROM evaluations ORDER BY created_at DESC").fetchall()
            return [row["id"] for row in rows]

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT 1 FROM evaluations WHERE id = ?", (key,)).fetchone()
            return row is not None

    def save_evaluation(self, evaluation_data: dict) -> str:
        """Save a complete evaluation result."""
        eval_id = evaluation_data.get("paper_id", "")
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO evaluations
                (id, paper_id, subject, strictness, total_awarded, total_possible,
                 percentage, question_count, evaluation_data, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                eval_id,
                eval_id,
                evaluation_data.get("subject", ""),
                evaluation_data.get("strictness", 6),
                evaluation_data.get("total_awarded", 0),
                evaluation_data.get("total_possible", 0),
                evaluation_data.get("percentage", 0),
                evaluation_data.get("question_count", 0),
                json.dumps(evaluation_data, default=str),
                datetime.now().isoformat(),
            ))

            # Save individual question evaluations
            for qe in evaluation_data.get("question_evaluations", []):
                conn.execute("""
                    INSERT INTO question_evaluations
                    (evaluation_id, question_number, question_text, answer_text, max_marks,
                     awarded_marks, model_answer, missing_content, improvements,
                     upsc_feedback, rubric_scores, strengths, weaknesses, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    eval_id,
                    qe.get("question_number", 0),
                    qe.get("question_text", ""),
                    qe.get("answer_text", ""),
                    qe.get("max_marks", 0),
                    qe.get("awarded_marks", 0),
                    qe.get("model_answer", ""),
                    json.dumps(qe.get("missing_content", [])),
                    json.dumps(qe.get("improvements", [])),
                    qe.get("upsc_feedback", ""),
                    json.dumps(qe.get("rubric_scores", [])),
                    json.dumps(qe.get("strengths", [])),
                    json.dumps(qe.get("weaknesses", [])),
                    datetime.now().isoformat(),
                ))

        logger.info(f"Saved evaluation: {eval_id}")
        return eval_id

    def save_attempt(self, attempt_data: dict) -> None:
        """Save an attempt record for analytics."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO attempts
                (paper_id, subject, strictness, total_awarded, total_possible,
                 percentage, component_averages, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                attempt_data.get("paper_id", ""),
                attempt_data.get("subject", ""),
                attempt_data.get("strictness", 6),
                attempt_data.get("total_awarded", 0),
                attempt_data.get("total_possible", 0),
                attempt_data.get("percentage", 0),
                json.dumps(attempt_data.get("component_averages", {})),
                datetime.now().isoformat(),
            ))

    def get_attempt_history(self, subject: str = "", limit: int = 50) -> list[dict]:
        """Get attempt history, optionally filtered by subject."""
        with self._get_connection() as conn:
            if subject:
                rows = conn.execute(
                    "SELECT * FROM attempts WHERE subject = ? ORDER BY created_at DESC LIMIT ?",
                    (subject, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM attempts ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            return [dict(row) for row in rows]

    def get_subject_averages(self) -> dict[str, float]:
        """Get average percentage by subject."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT subject, AVG(percentage) as avg_pct, COUNT(*) as count
                FROM attempts
                GROUP BY subject
                ORDER BY avg_pct DESC
            """).fetchall()
            return {row["subject"]: round(row["avg_pct"], 1) for row in rows}

    def get_evaluation_count(self) -> int:
        """Get total evaluation count."""
        with self._get_connection() as conn:
            row = conn.execute("SELECT COUNT(*) as cnt FROM attempts").fetchone()
            return row["cnt"] if row else 0
