from __future__ import annotations

import hashlib
import json
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import psycopg
from psycopg.rows import dict_row


DB_HOST = os.environ["DATABASE_HOST"]
DB_PORT = int(os.environ.get("DATABASE_PORT", "5432"))
DB_NAME = os.environ["DATABASE_NAME"]
DB_USER = os.environ["DATABASE_USER"]
DB_PASSWORD = os.environ["DATABASE_PASSWORD"]
AUDIT_PATH = Path(os.environ.get("AUDIT_LOG_PATH", "/var/log/company-owned-cloud/audit.jsonl"))


def dsn() -> str:
    return f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} connect_timeout=3"


@contextmanager
def connection() -> Iterator[psycopg.Connection]:
    with psycopg.connect(dsn(), row_factory=dict_row) as database:
        yield database


def migrate() -> None:
    last_error: Exception | None = None
    for _ in range(40):
        try:
            with connection() as database:
                database.execute(
                    """
                    CREATE TABLE IF NOT EXISTS notes (
                        id BIGSERIAL PRIMARY KEY,
                        title TEXT NOT NULL CHECK (char_length(title) BETWEEN 1 AND 120),
                        body TEXT NOT NULL CHECK (char_length(body) BETWEEN 1 AND 4000),
                        created_by TEXT NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                    );
                    CREATE TABLE IF NOT EXISTS audit_events (
                        id BIGSERIAL PRIMARY KEY,
                        occurred_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                        request_id TEXT NOT NULL,
                        subject_hash TEXT NOT NULL,
                        action TEXT NOT NULL,
                        outcome TEXT NOT NULL,
                        target TEXT NOT NULL
                    );
                    """
                )
                database.commit()
            AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
            return
        except Exception as error:
            last_error = error
            time.sleep(1)
    raise RuntimeError(f"database migration unavailable: {type(last_error).__name__}")


def subject_hash(subject: str) -> str:
    return hashlib.sha256(subject.encode("utf-8")).hexdigest()[:16]


def write_audit(request_id: str, subject: str, action: str, outcome: str, target: str) -> None:
    record = {
        "request_id": request_id,
        "subject_hash": subject_hash(subject),
        "action": action,
        "outcome": outcome,
        "target": target,
    }
    with connection() as database:
        database.execute(
            "INSERT INTO audit_events(request_id, subject_hash, action, outcome, target) VALUES (%s, %s, %s, %s, %s)",
            (record["request_id"], record["subject_hash"], action, outcome, target),
        )
        database.commit()
    with AUDIT_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")


def state_summary() -> dict[str, int | str]:
    with connection() as database:
        rows = database.execute(
            "SELECT title, body, created_by FROM notes ORDER BY title, body, created_by"
        ).fetchall()
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return {"record_count": len(rows), "content_sha256": hashlib.sha256(canonical).hexdigest()}


def audit_safety() -> dict[str, int | bool]:
    allowed_keys = {"request_id", "subject_hash", "action", "outcome", "target"}
    event_count = 0
    safe = True
    if AUDIT_PATH.exists():
        for line in AUDIT_PATH.read_text(encoding="utf-8").splitlines():
            event_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                safe = False
                continue
            if set(record) != allowed_keys:
                safe = False
            serialised = json.dumps(record).lower()
            if "bearer " in serialised or "password" in serialised or "note_body" in serialised:
                safe = False
    return {"safe": safe, "event_count": event_count}
