from __future__ import annotations

from dataclasses import dataclass

from ..models import JobPosting


@dataclass(frozen=True)
class MatchResult:
    score: int
    reason: str
    keywords_found: list[str]


def score_job(job: JobPosting, profile: dict) -> MatchResult:
    base_score = int(profile.get("base_score", 40))
    score = base_score
    found: list[str] = []
    reasons: list[str] = []

    all_text = job.searchable_text().lower()
    title_text = job.title.lower()
    location_text = job.location.lower()

    for keyword, weight in profile.get("positive_keywords", {}).items():
        key = keyword.lower()
        if key in all_text:
            adjusted_weight = int(weight)
            if key in title_text or key in profile.get("title_boost_keywords", []):
                adjusted_weight += 2 if key in title_text else 0
            score += adjusted_weight
            found.append(keyword)

    for keyword, weight in profile.get("negative_keywords", {}).items():
        key = keyword.lower()
        if key in all_text:
            score += int(weight)
            found.append(keyword)

    if job.remote is True:
        score += 6
        reasons.append("remote")

    for location in profile.get("preferred_locations", []):
        key = str(location).lower()
        if key in location_text:
            score += 4
            reasons.append(f"location: {location}")

    score = max(0, min(100, score))

    positives = [
        keyword
        for keyword in found
        if keyword in profile.get("positive_keywords", {})
    ]
    negatives = [
        keyword
        for keyword in found
        if keyword in profile.get("negative_keywords", {})
    ]

    if positives:
        reasons.append("matches: " + ", ".join(positives[:6]))
    if negatives:
        reasons.append("risks: " + ", ".join(negatives[:4]))
    if not reasons:
        reasons.append("no strong profile signals")

    return MatchResult(
        score=score,
        reason="; ".join(reasons),
        keywords_found=found,
    )
