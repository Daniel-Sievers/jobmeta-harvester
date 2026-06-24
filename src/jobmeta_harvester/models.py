from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class JobPosting:
    source: str
    source_id: str
    title: str
    company: str
    location: str
    remote: bool | None
    url: str
    date_posted: str
    description: str
    tags: list[str] = field(default_factory=list)

    def searchable_text(self) -> str:
        parts = [
            self.title,
            self.company,
            self.location,
            self.description,
            " ".join(self.tags),
        ]
        return " ".join(part for part in parts if part)
