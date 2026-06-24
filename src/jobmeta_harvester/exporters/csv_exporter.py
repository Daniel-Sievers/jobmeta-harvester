from __future__ import annotations

import csv
from pathlib import Path

from ..matching import score_job
from ..models import JobPosting


CSV_FIELDS = [
    "job_key",
    "match_score",
    "match_reason",
    "source",
    "source_id",
    "title",
    "company",
    "location",
    "location_remote_start",
    "remote",
    "date_posted",
    "url",
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
    "keywords_found",
    "tags",
    "application_status",
    "priority",
    "application_deadline",
    "next_action",
    "notes",
    "first_seen",
    "last_seen",
    "seen_count",
]


def export_jobs_csv(jobs: list[JobPosting], profile: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scored_rows = []
    for job in jobs:
        match = score_job(job, profile)
        scored_rows.append((match.score, job, match))

    scored_rows.sort(key=lambda item: item[0], reverse=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for _, job, match in scored_rows:
            writer.writerow(
                {
                    "job_key": "",
                    "match_score": match.score,
                    "match_reason": match.reason,
                    "source": job.source,
                    "source_id": job.source_id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "location_remote_start": "",
                    "remote": _format_remote(job.remote),
                    "date_posted": job.date_posted,
                    "url": job.url,
                    "role_cluster": "",
                    "industry": "",
                    "main_tasks": "",
                    "work_pattern": "",
                    "tools_systems": "",
                    "must_skills": "",
                    "nice_to_have": "",
                    "already_have": "",
                    "gap_blocking": "",
                    "gap_learnable": "",
                    "gap_bonus": "",
                    "experience_required": "",
                    "entry_realistic": "",
                    "growth_value": "",
                    "interest": "",
                    "decision": "",
                    "keywords_found": ", ".join(match.keywords_found),
                    "tags": ", ".join(job.tags),
                    "application_status": "",
                    "priority": "",
                    "application_deadline": "",
                    "next_action": "",
                    "notes": "",
                    "first_seen": "",
                    "last_seen": "",
                    "seen_count": "",
                }
            )


def export_records_csv(records: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "job_key": record.get("job_key", ""),
                    "match_score": record.get("match_score", ""),
                    "match_reason": record.get("match_reason", ""),
                    "source": record.get("source", ""),
                    "source_id": record.get("source_id", ""),
                    "title": record.get("title", ""),
                    "company": record.get("company", ""),
                    "location": record.get("location", ""),
                    "location_remote_start": record.get("location_remote_start", ""),
                    "remote": _format_remote_int(record.get("remote")),
                    "date_posted": record.get("date_posted", ""),
                    "url": record.get("url", ""),
                    "role_cluster": record.get("role_cluster", ""),
                    "industry": record.get("industry", ""),
                    "main_tasks": record.get("main_tasks", ""),
                    "work_pattern": record.get("work_pattern", ""),
                    "tools_systems": record.get("tools_systems", ""),
                    "must_skills": record.get("must_skills", ""),
                    "nice_to_have": record.get("nice_to_have", ""),
                    "already_have": record.get("already_have", ""),
                    "gap_blocking": record.get("gap_blocking", ""),
                    "gap_learnable": record.get("gap_learnable", ""),
                    "gap_bonus": record.get("gap_bonus", ""),
                    "experience_required": record.get("experience_required", ""),
                    "entry_realistic": record.get("entry_realistic", ""),
                    "growth_value": record.get("growth_value", ""),
                    "interest": record.get("interest", ""),
                    "decision": record.get("decision", ""),
                    "keywords_found": record.get("keywords_found", ""),
                    "tags": record.get("tags", ""),
                    "application_status": record.get("application_status", ""),
                    "priority": record.get("priority", ""),
                    "application_deadline": record.get("application_deadline", ""),
                    "next_action": record.get("next_action", ""),
                    "notes": record.get("notes", ""),
                    "first_seen": record.get("first_seen", ""),
                    "last_seen": record.get("last_seen", ""),
                    "seen_count": record.get("seen_count", ""),
                }
            )


def _format_remote(value: bool | None) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    return ""


def _format_remote_int(value: int | None) -> str:
    if value == 1:
        return "yes"
    if value == 0:
        return "no"
    return ""
