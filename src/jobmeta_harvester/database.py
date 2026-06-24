from __future__ import annotations

import csv
import io
import re
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

from .matching import score_job
from .models import JobPosting


ANALYSIS_FIELDS = [
    "role_cluster",
    "location_remote_start",
    "industry",
    "main_tasks",
    "work_pattern",
    "tools_systems",
    "must_skills",
    "nice_to_have",
    "already_have",
    "gap_blocking",
    "gap_learnable",
    "gap_bonus",
    "experience_required",
    "entry_realistic",
    "growth_value",
    "interest",
    "decision",
]

WORKFLOW_FIELDS = [
    "priority",
    "application_deadline",
    "next_action",
]

EDITABLE_FIELDS = {
    "application_status",
    "notes",
    "url",
    "decision",
    "interest",
    "entry_realistic",
    "growth_value",
    "priority",
    "application_deadline",
    "next_action",
}

CSV_ALIASES = {
    "quelle": "source",
    "source": "source",
    "nr.": "source_id",
    "nr": "source_id",
    "id": "source_id",
    "unternehmen": "company",
    "unternehmen / link": "company",
    "company": "company",
    "firma": "company",
    "link": "url",
    "url": "url",
    "anzeige": "url",
    "jobtitel": "title",
    "job_title": "title",
    "title": "title",
    "titel": "title",
    "rollencluster": "role_cluster",
    "rollenclus ter": "role_cluster",
    "role_cluster": "role_cluster",
    "ort / remote / start": "location_remote_start",
    "ort": "location_remote_start",
    "location": "location_remote_start",
    "location_remote_start": "location_remote_start",
    "branche": "industry",
    "industry": "industry",
    "hauptaufgaben": "main_tasks",
    "main_tasks": "main_tasks",
    "muster": "work_pattern",
    "work_pattern": "work_pattern",
    "tools / systeme": "tools_systems",
    "tools": "tools_systems",
    "tools_systems": "tools_systems",
    "muss-skills": "must_skills",
    "must_skills": "must_skills",
    "kann-skills": "nice_to_have",
    "nice_to_have": "nice_to_have",
    "was kann ich schon?": "already_have",
    "already_have": "already_have",
    "lücken a blockierend": "gap_blocking",
    "luecken a blockierend": "gap_blocking",
    "gap_blocking": "gap_blocking",
    "lücken b schnell lernbar": "gap_learnable",
    "luecken b schnell lernbar": "gap_learnable",
    "gap_learnable": "gap_learnable",
    "lücken c entwicklung / bonus": "gap_bonus",
    "luecken c entwicklung / bonus": "gap_bonus",
    "gap_bonus": "gap_bonus",
    "erfahrung": "experience_required",
    "experience_required": "experience_required",
    "einstieg realistisch?": "entry_realistic",
    "entry_realistic": "entry_realistic",
    "wachstum wert": "growth_value",
    "wachstumswert": "growth_value",
    "growth_value": "growth_value",
    "interesse": "interest",
    "interest": "interest",
    "entscheidung": "decision",
    "decision": "decision",
    "notiz": "notes",
    "notizen": "notes",
    "notes": "notes",
    "prioritaet": "priority",
    "priorität": "priority",
    "priority": "priority",
    "bewerbungsfrist": "application_deadline",
    "frist": "application_deadline",
    "deadline": "application_deadline",
    "application_deadline": "application_deadline",
    "naechste aktion": "next_action",
    "nächste aktion": "next_action",
    "next action": "next_action",
    "next_action": "next_action",
    "application_status": "application_status",
    "status": "application_status",
    "tags": "tags",
    "description": "description",
    "beschreibung": "description",
    "date_posted": "date_posted",
    "datum": "date_posted",
    "remote": "remote",
}


SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    job_key TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    remote INTEGER,
    url TEXT NOT NULL,
    date_posted TEXT NOT NULL,
    description TEXT NOT NULL,
    tags TEXT NOT NULL,
    match_score INTEGER NOT NULL,
    match_reason TEXT NOT NULL,
    keywords_found TEXT NOT NULL,
    application_status TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    priority TEXT NOT NULL DEFAULT '',
    application_deadline TEXT NOT NULL DEFAULT '',
    next_action TEXT NOT NULL DEFAULT '',
    role_cluster TEXT NOT NULL DEFAULT '',
    location_remote_start TEXT NOT NULL DEFAULT '',
    industry TEXT NOT NULL DEFAULT '',
    main_tasks TEXT NOT NULL DEFAULT '',
    work_pattern TEXT NOT NULL DEFAULT '',
    tools_systems TEXT NOT NULL DEFAULT '',
    must_skills TEXT NOT NULL DEFAULT '',
    nice_to_have TEXT NOT NULL DEFAULT '',
    already_have TEXT NOT NULL DEFAULT '',
    gap_blocking TEXT NOT NULL DEFAULT '',
    gap_learnable TEXT NOT NULL DEFAULT '',
    gap_bonus TEXT NOT NULL DEFAULT '',
    experience_required TEXT NOT NULL DEFAULT '',
    entry_realistic TEXT NOT NULL DEFAULT '',
    growth_value TEXT NOT NULL DEFAULT '',
    interest TEXT NOT NULL DEFAULT '',
    decision TEXT NOT NULL DEFAULT '',
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    seen_count INTEGER NOT NULL DEFAULT 1
);
"""


def init_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with _connect(db_path) as connection:
        connection.execute(SCHEMA)
        _migrate_columns(connection)


def upsert_jobs(jobs: list[JobPosting], profile: dict, db_path: Path) -> dict[str, int]:
    records = [_record_from_job(job) for job in jobs]
    return upsert_job_records(records, profile, db_path, update_tracking_fields=False)


def upsert_job_records(
    records: list[dict[str, Any]],
    profile: dict,
    db_path: Path,
    update_tracking_fields: bool = True,
) -> dict[str, int]:
    init_db(db_path)
    now = _now()
    stats = {"incoming": len(records), "new": 0, "updated": 0, "duplicates": 0}
    seen_in_run: set[str] = set()

    with _connect(db_path) as connection:
        for record in records:
            record = _normalize_record(record)
            job = _job_from_record(record)
            job_key = make_job_key(job)
            if job_key in seen_in_run:
                stats["duplicates"] += 1
                continue
            seen_in_run.add(job_key)

            match = score_job(job, profile)
            existing = connection.execute(
                "SELECT job_key FROM jobs WHERE job_key = ?",
                (job_key,),
            ).fetchone()
            if existing:
                stats["updated"] += 1
                tracking_sql = ""
                tracking_values: tuple[Any, ...] = ()
                if update_tracking_fields:
                    tracking_sql = """
                        application_status = CASE WHEN ? != '' THEN ? ELSE application_status END,
                        notes = CASE WHEN ? != '' THEN ? ELSE notes END,
                        priority = CASE WHEN ? != '' THEN ? ELSE priority END,
                        application_deadline = CASE WHEN ? != '' THEN ? ELSE application_deadline END,
                        next_action = CASE WHEN ? != '' THEN ? ELSE next_action END,
                    """
                    tracking_values = (
                        record.get("application_status", ""),
                        record.get("application_status", ""),
                        record.get("notes", ""),
                        record.get("notes", ""),
                        record.get("priority", ""),
                        record.get("priority", ""),
                        record.get("application_deadline", ""),
                        record.get("application_deadline", ""),
                        record.get("next_action", ""),
                        record.get("next_action", ""),
                    )
                connection.execute(
                    f"""
                    UPDATE jobs
                    SET source = ?,
                        source_id = ?,
                        title = ?,
                        company = ?,
                        location = ?,
                        remote = ?,
                        url = ?,
                        date_posted = ?,
                        description = ?,
                        tags = ?,
                        match_score = ?,
                        match_reason = ?,
                        keywords_found = ?,
                        {tracking_sql}
                        role_cluster = ?,
                        location_remote_start = ?,
                        industry = ?,
                        main_tasks = ?,
                        work_pattern = ?,
                        tools_systems = ?,
                        must_skills = ?,
                        nice_to_have = ?,
                        already_have = ?,
                        gap_blocking = ?,
                        gap_learnable = ?,
                        gap_bonus = ?,
                        experience_required = ?,
                        entry_realistic = ?,
                        growth_value = ?,
                        interest = ?,
                        decision = ?,
                        last_seen = ?,
                        seen_count = seen_count + 1
                    WHERE job_key = ?
                    """,
                    _job_values(job, match) + tracking_values + _analysis_values(record) + (now, job_key),
                )
            else:
                stats["new"] += 1
                connection.execute(
                    """
                    INSERT INTO jobs (
                        job_key, source, source_id, title, company, location,
                        remote, url, date_posted, description, tags,
                        match_score, match_reason, keywords_found,
                        application_status, notes,
                        priority, application_deadline, next_action,
                        role_cluster, location_remote_start, industry,
                        main_tasks, work_pattern, tools_systems,
                        must_skills, nice_to_have, already_have,
                        gap_blocking, gap_learnable, gap_bonus,
                        experience_required, entry_realistic,
                        growth_value, interest, decision,
                        first_seen, last_seen, seen_count
                    )
                    VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, 1
                    )
                    """,
                    (
                        job_key,
                    )
                    + _job_values(job, match)
                    + (
                        record.get("application_status", ""),
                        record.get("notes", ""),
                    )
                    + _workflow_values(record)
                    + _analysis_values(record)
                    + (now, now),
                )
    return stats


def import_jobs_csv(csv_path: Path, profile: dict, db_path: Path) -> dict[str, int]:
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        return import_jobs_csv_text(handle.read(), profile, db_path)


def import_jobs_csv_text(csv_text: str, profile: dict, db_path: Path) -> dict[str, int]:
    reader = csv.DictReader(io.StringIO(csv_text))
    records = [_row_to_record(row) for row in reader]
    return upsert_job_records(records, profile, db_path, update_tracking_fields=True)


def list_jobs(db_path: Path) -> list[dict[str, Any]]:
    init_db(db_path)
    with _connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM jobs
            ORDER BY match_score DESC, date_posted DESC, title ASC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def delete_jobs_by_source_prefixes(db_path: Path, prefixes: list[str]) -> int:
    init_db(db_path)
    if not prefixes:
        return 0
    deleted = 0
    with _connect(db_path) as connection:
        for prefix in prefixes:
            cursor = connection.execute(
                "DELETE FROM jobs WHERE source = ? OR source LIKE ?",
                (prefix, f"{prefix}-%"),
            )
            deleted += cursor.rowcount
    return deleted


def delete_all_jobs(db_path: Path) -> int:
    """Delete all job records while keeping the database schema and profile files intact."""
    init_db(db_path)
    with _connect(db_path) as connection:
        cursor = connection.execute("DELETE FROM jobs")
    return cursor.rowcount


def rescore_jobs(profile: dict, db_path: Path) -> int:
    init_db(db_path)
    updated = 0
    with _connect(db_path) as connection:
        rows = connection.execute("SELECT * FROM jobs").fetchall()
        for row in rows:
            job = _job_from_db_row(dict(row))
            match = score_job(job, profile)
            cursor = connection.execute(
                """
                UPDATE jobs
                SET match_score = ?,
                    match_reason = ?,
                    keywords_found = ?
                WHERE job_key = ?
                """,
                (
                    match.score,
                    match.reason,
                    ", ".join(match.keywords_found),
                    row["job_key"],
                ),
            )
            updated += cursor.rowcount
    return updated


def import_tracking_csv(csv_path: Path, db_path: Path) -> int:
    init_db(db_path)
    updated = 0
    with csv_path.open(newline="", encoding="utf-8") as handle, _connect(db_path) as connection:
        reader = csv.DictReader(handle)
        for row in reader:
            job_key = row.get("job_key") or ""
            if not job_key:
                job_key = make_job_key(
                    JobPosting(
                        source=row.get("source", ""),
                        source_id=row.get("source_id", ""),
                        title=row.get("title", ""),
                        company=row.get("company", ""),
                        location=row.get("location", ""),
                        remote=None,
                        url=row.get("url", ""),
                        date_posted=row.get("date_posted", ""),
                        description="",
                        tags=[],
                    )
                )
            status = row.get("application_status", "")
            notes = row.get("notes", "")
            priority = row.get("priority", "")
            application_deadline = row.get("application_deadline", "")
            next_action = row.get("next_action", "")
            cursor = connection.execute(
                """
                UPDATE jobs
                SET application_status = ?,
                    notes = ?,
                    priority = ?,
                    application_deadline = ?,
                    next_action = ?
                WHERE job_key = ?
                """,
                (status, notes, priority, application_deadline, next_action, job_key),
            )
            updated += cursor.rowcount
    return updated


def update_tracking(
    db_path: Path,
    job_key: str,
    application_status: str | None = None,
    notes: str | None = None,
    decision: str | None = None,
    interest: str | None = None,
    entry_realistic: str | None = None,
    growth_value: str | None = None,
    priority: str | None = None,
    application_deadline: str | None = None,
    next_action: str | None = None,
    url: str | None = None,
    extra_fields: dict[str, str] | None = None,
) -> bool:
    init_db(db_path)
    updates: list[str] = []
    values: list[str] = []
    field_values = {
        "application_status": application_status,
        "notes": notes,
        "decision": decision,
        "interest": interest,
        "entry_realistic": entry_realistic,
        "growth_value": growth_value,
        "priority": priority,
        "application_deadline": application_deadline,
        "next_action": next_action,
        "url": url,
    }
    if extra_fields:
        field_values.update(extra_fields)
    for field, value in field_values.items():
        if field in EDITABLE_FIELDS and value is not None:
            updates.append(f"{field} = ?")
            values.append(value)
    if not updates:
        return False

    values.append(job_key)
    with _connect(db_path) as connection:
        cursor = connection.execute(
            f"UPDATE jobs SET {', '.join(updates)} WHERE job_key = ?",
            values,
        )
    return cursor.rowcount > 0


def make_job_key(job: JobPosting) -> str:
    title = _slug(job.title)
    company = _slug(job.company)
    location = _slug(job.location)
    if title and company:
        return "|".join([title, company, location])
    return "|".join([_slug(job.source), _slug(job.source_id), _slug(job.url)])


@contextmanager
def _connect(db_path: Path) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()


def _migrate_columns(connection: sqlite3.Connection) -> None:
    existing = {
        row["name"]
        for row in connection.execute("PRAGMA table_info(jobs)").fetchall()
    }
    for field in ANALYSIS_FIELDS + WORKFLOW_FIELDS:
        if field not in existing:
            connection.execute(
                f"ALTER TABLE jobs ADD COLUMN {field} TEXT NOT NULL DEFAULT ''"
            )


def _job_values(job: JobPosting, match: Any) -> tuple[Any, ...]:
    return (
        job.source,
        job.source_id,
        job.title,
        job.company,
        job.location,
        _remote_to_int(job.remote),
        job.url,
        job.date_posted,
        job.description,
        ", ".join(job.tags),
        match.score,
        match.reason,
        ", ".join(match.keywords_found),
    )


def _analysis_values(record: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(record.get(field, "") or "") for field in ANALYSIS_FIELDS)


def _workflow_values(record: dict[str, Any]) -> tuple[str, ...]:
    return tuple(str(record.get(field, "") or "") for field in WORKFLOW_FIELDS)


def _record_from_job(job: JobPosting) -> dict[str, Any]:
    return {
        "source": job.source,
        "source_id": job.source_id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "remote": job.remote,
        "url": job.url,
        "date_posted": job.date_posted,
        "description": job.description,
        "tags": ", ".join(job.tags),
    }


def _job_from_record(record: dict[str, Any]) -> JobPosting:
    tags = [tag.strip() for tag in str(record.get("tags", "")).split(",") if tag.strip()]
    location = record.get("location") or record.get("location_remote_start", "")
    description = record.get("description") or _description_from_record(record)
    return JobPosting(
        source=str(record.get("source", "") or "manual"),
        source_id=str(record.get("source_id", "") or record.get("url", "")),
        title=str(record.get("title", "")),
        company=str(record.get("company", "")),
        location=str(location),
        remote=_parse_remote(record.get("remote") or location),
        url=str(record.get("url", "")),
        date_posted=str(record.get("date_posted", "")),
        description=str(description),
        tags=tags,
    )


def _job_from_db_row(row: dict[str, Any]) -> JobPosting:
    description_parts = [str(row.get("description", "") or "")]
    description_parts.extend(str(row.get(field, "") or "") for field in ANALYSIS_FIELDS)
    return JobPosting(
        source=str(row.get("source", "") or ""),
        source_id=str(row.get("source_id", "") or ""),
        title=str(row.get("title", "") or ""),
        company=str(row.get("company", "") or ""),
        location=str(row.get("location", "") or row.get("location_remote_start", "") or ""),
        remote=_int_to_remote(row.get("remote")),
        url=str(row.get("url", "") or ""),
        date_posted=str(row.get("date_posted", "") or ""),
        description=" ".join(description_parts),
        tags=[tag.strip() for tag in str(row.get("tags", "") or "").split(",") if tag.strip()],
    )


def _description_from_record(record: dict[str, Any]) -> str:
    fields = [
        "role_cluster",
        "industry",
        "main_tasks",
        "work_pattern",
        "tools_systems",
        "must_skills",
        "nice_to_have",
        "already_have",
        "gap_blocking",
        "gap_learnable",
        "gap_bonus",
        "experience_required",
        "entry_realistic",
        "growth_value",
        "interest",
        "decision",
        "priority",
        "application_deadline",
        "next_action",
        "notes",
    ]
    return " ".join(str(record.get(field, "") or "") for field in fields)


def _row_to_record(row: dict[str, Any]) -> dict[str, Any]:
    record: dict[str, Any] = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = _normalize_header(raw_key)
        target = CSV_ALIASES.get(key, key)
        record[target] = str(value or "").strip()
    if not record.get("source"):
        record["source"] = "csv"
    if not record.get("source_id"):
        record["source_id"] = record.get("url", "")
    if not record.get("location") and record.get("location_remote_start"):
        record["location"] = record["location_remote_start"]
    return record


def _normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    normalized = {key: ("" if value is None else value) for key, value in record.items()}
    if not normalized.get("source"):
        normalized["source"] = "manual"
    if not normalized.get("source_id"):
        normalized["source_id"] = normalized.get("url", "")
    if not normalized.get("location") and normalized.get("location_remote_start"):
        normalized["location"] = normalized["location_remote_start"]
    return normalized


def _normalize_header(value: str) -> str:
    text = value.strip().lower().replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def _parse_remote(value: Any) -> bool | None:
    text = str(value or "").lower()
    if any(word in text for word in ["remote", "homeoffice", "home office", "hybrid"]):
        return True
    if text in {"yes", "true", "1", "ja"}:
        return True
    if text in {"no", "false", "0", "nein"}:
        return False
    return None


def _remote_to_int(value: bool | None) -> int | None:
    if value is True:
        return 1
    if value is False:
        return 0
    return None


def _int_to_remote(value: Any) -> bool | None:
    if value == 1:
        return True
    if value == 0:
        return False
    return None


def _slug(value: str) -> str:
    text = value.lower().strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z0-9äöüß /+_.-]+", "", text)
    return text


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
