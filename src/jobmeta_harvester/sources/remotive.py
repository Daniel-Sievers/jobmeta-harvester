from __future__ import annotations

from urllib.parse import urlencode

from ..http import fetch_json
from ..models import JobPosting
from ..normalization import clean_tags, clean_text


API_URL = "https://remotive.com/api/remote-jobs"


def fetch_remotive_jobs(limit: int = 50, query: list[str] | None = None) -> list[JobPosting]:
    params = {"limit": str(limit)}
    if query:
        params["search"] = " ".join(query)
    url = f"{API_URL}?{urlencode(params)}"
    payload = fetch_json(url)
    rows = payload.get("jobs", []) if isinstance(payload, dict) else []
    return [_normalize(row) for row in rows[:limit]]


def _normalize(row: dict) -> JobPosting:
    tags = clean_tags(row.get("tags"))
    category = clean_text(row.get("category"))
    job_type = clean_text(row.get("job_type"))
    for tag in [category, job_type]:
        if tag and tag.lower() not in {existing.lower() for existing in tags}:
            tags.append(tag)
    return JobPosting(
        source="remotive",
        source_id=clean_text(row.get("id")),
        title=clean_text(row.get("title")),
        company=clean_text(row.get("company_name")),
        location=clean_text(row.get("candidate_required_location")),
        remote=True,
        url=clean_text(row.get("url")),
        date_posted=clean_text(row.get("publication_date")),
        description=clean_text(row.get("description")),
        tags=tags,
    )
