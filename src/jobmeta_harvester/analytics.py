from __future__ import annotations

import re
from collections import Counter
from typing import Any


SPLIT_RE = re.compile(r"[,;\n•]+|\s+-\s+")
SPACE_RE = re.compile(r"\s+")
TRIM_RE = re.compile(r"^[\W_]+|[\W_]+$")

STOP_TERMS = {
    "",
    "none",
    "keine",
    "n/a",
    "-",
    "unklar",
    "nicht eindeutig",
}


def build_skill_gap_summary(records: list[dict[str, Any]], top_n: int = 8) -> dict[str, Any]:
    total_jobs = len(records)
    strong_jobs = sum(1 for row in records if int(row.get("match_score") or 0) >= 70)
    return {
        "total_jobs": total_jobs,
        "strong_jobs": strong_jobs,
        "blocking_gaps": _top_terms(records, "gap_blocking", top_n),
        "learnable_gaps": _top_terms(records, "gap_learnable", top_n),
        "bonus_gaps": _top_terms(records, "gap_bonus", top_n),
        "must_skills": _top_terms(records, "must_skills", top_n),
        "tools": _top_terms(records, "tools_systems", top_n),
        "already_have": _top_terms(records, "already_have", top_n),
        "learning_priorities": _learning_priorities(records, top_n),
    }


def _learning_priorities(records: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    learnable = _counter_for(records, "gap_learnable")
    must = _counter_for(records, "must_skills")
    combined: Counter[str] = Counter()
    display_names: dict[str, str] = {}
    for key, count in learnable.items():
        combined[key] += count * 2
    for key, count in must.items():
        combined[key] += count
    for row in records:
        for field in ["gap_learnable", "must_skills"]:
            for term in _terms(row.get(field, "")):
                display_names.setdefault(_normalize(term), term)
    return [
        {"label": display_names.get(key, key), "count": value}
        for key, value in combined.most_common(top_n)
    ]


def _top_terms(records: list[dict[str, Any]], field: str, top_n: int) -> list[dict[str, Any]]:
    counter = _counter_for(records, field)
    display_names: dict[str, str] = {}
    for row in records:
        for term in _terms(row.get(field, "")):
            display_names.setdefault(_normalize(term), term)
    return [
        {"label": display_names.get(key, key), "count": value}
        for key, value in counter.most_common(top_n)
    ]


def _counter_for(records: list[dict[str, Any]], field: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for row in records:
        for term in _terms(row.get(field, "")):
            counter[_normalize(term)] += 1
    return counter


def _terms(value: Any) -> list[str]:
    text = str(value or "")
    parts = SPLIT_RE.split(text)
    terms = []
    for part in parts:
        term = TRIM_RE.sub("", SPACE_RE.sub(" ", part).strip())
        if not term:
            continue
        if _normalize(term) in STOP_TERMS:
            continue
        if len(term) < 3:
            continue
        terms.append(term)
    return terms


def _normalize(value: str) -> str:
    return SPACE_RE.sub(" ", value.strip().lower())
