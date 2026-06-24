from __future__ import annotations

from urllib.parse import urlencode

from ..http import fetch_json
from ..models import JobPosting
from ..normalization import clean_tags, clean_text, unix_to_date


API_URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_arbeitnow_jobs(limit: int = 50, query: list[str] | None = None) -> list[JobPosting]:
    params = {}
    if query:
        params["search"] = " ".join(query)
    url = API_URL if not params else f"{API_URL}?{urlencode(params)}"
    payload = fetch_json(url)
    rows = payload.get("data", []) if isinstance(payload, dict) else []
    return [_normalize(row) for row in rows[:limit]]


def _normalize(row: dict) -> JobPosting:
    tags = clean_tags(row.get("tags")) + clean_tags(row.get("job_types"))
    slug = clean_text(row.get("slug") or row.get("id") or row.get("url"))
    return JobPosting(
        source="arbeitnow",
        source_id=slug,
        title=clean_text(row.get("title")),
        company=clean_text(row.get("company_name") or row.get("company")),
        location=clean_text(row.get("location")),
        remote=_to_bool(row.get("remote")),
        url=clean_text(row.get("url")),
        date_posted=unix_to_date(row.get("created_at") or row.get("created_at_timestamp")),
        description=clean_text(row.get("description")),
        tags=tags,
    )


def _to_bool(value: object) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "remote"}:
        return True
    if text in {"0", "false", "no"}:
        return False
    return None
