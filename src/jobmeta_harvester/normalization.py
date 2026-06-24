from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from typing import Any


TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = html.unescape(str(value))
    text = TAG_RE.sub(" ", text)
    return WHITESPACE_RE.sub(" ", text).strip()


def clean_tags(value: Any) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        raw_tags = [value]
    else:
        raw_tags = list(value)
    seen: set[str] = set()
    tags: list[str] = []
    for item in raw_tags:
        tag = clean_text(item)
        key = tag.lower()
        if tag and key not in seen:
            seen.add(key)
            tags.append(tag)
    return tags


def unix_to_date(value: Any) -> str:
    try:
        timestamp = int(value)
    except (TypeError, ValueError):
        return clean_text(value)
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()
