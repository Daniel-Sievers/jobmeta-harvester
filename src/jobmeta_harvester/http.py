from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


USER_AGENT = "JobMetaHarvester/0.1 portfolio project"


class FetchError(RuntimeError):
    """Raised when a remote job source cannot be fetched."""


def fetch_json(url: str, timeout: int = 20) -> dict:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except HTTPError as exc:
        raise FetchError(f"HTTP {exc.code} while fetching {url}") from exc
    except URLError as exc:
        raise FetchError(f"Network error while fetching {url}: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise FetchError(f"Invalid JSON from {url}") from exc
