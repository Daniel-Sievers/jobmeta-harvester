from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "vercel.json",
    "package.json",
    "index.html",
    "app/index.html",
    "demo/index.html",
    "static-api-shim.js",
    "manifest.webmanifest",
    "service-worker.js",
    "offline.html",
    "version.json",
    "local/index.html",
    "assets/icon-192.png",
    "assets/icon-512.png",
    "data/static-api-data.json",
    "demo/check/index.html",
]


def fail(message: str) -> None:
    print(f"PWA check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).exists()]
    if missing:
        fail("missing files: " + ", ".join(missing))

    obsolete_files = [
        "app.js",
        "demo/app.js",
        "demo/app.css",
        "demo/manifest.webmanifest",
        "demo/service-worker.js",
        "demo/version.json",
        "demo/offline.html",
        "data/demo-data.json",
        "demo/data/demo-data.json",
        "demo/assets",
    ]
    present_obsolete = [path for path in obsolete_files if (ROOT / path).exists()]
    if present_obsolete:
        fail("obsolete separate demo files still present: " + ", ".join(present_obsolete))

    vercel = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    rewrites = {(item.get("source"), item.get("destination")) for item in vercel.get("rewrites", [])}
    for pair in [("/", "/index.html"), ("/app", "/app/index.html"), ("/demo", "/demo/index.html"), ("/demo/check", "/demo/check/index.html"), ("/local", "/local/index.html")]:
        if pair not in rewrites:
            fail(f"vercel.json missing route {pair}")

    manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("display") != "standalone":
        fail("manifest display must be standalone")
    if manifest.get("start_url") != "/app/" or manifest.get("scope") != "/":
        fail("manifest start_url should point to /app/ and scope should be /")
    icon_sizes = {icon.get("sizes") for icon in manifest.get("icons", [])}
    if "192x192" not in icon_sizes or "512x512" not in icon_sizes:
        fail("manifest must include 192x192 and 512x512 icons")

    root_html = (ROOT / "index.html").read_text(encoding="utf-8")
    for marker in ["Demo ansehen", "Werkzeug öffnen", "./demo/", "./app/"]:
        if marker not in root_html:
            fail(f"root selector is missing marker: {marker}")


    local_html = (ROOT / "local" / "index.html").read_text(encoding="utf-8")
    for marker in ["Lokale Vollversion", "python -m jobmeta_harvester --dashboard", "SQLite"]:
        if marker not in local_html:
            fail(f"local full-version page missing marker: {marker}")

    app_html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
    demo_html = (ROOT / "demo" / "index.html").read_text(encoding="utf-8")
    for html, name in [(app_html, "app"), (demo_html, "demo")]:
        for marker in ["JobMeta Dashboard", "Demo-Daten laden", "demoBackdrop", "quick-actions", "table-wrap", "Status und Notizen", "/static-api-shim.js", "horizontal-scroll-dock"]:
            if marker not in html:
                fail(f"{name} app is missing dashboard marker: {marker}")
        for obsolete in ["Jobanzeigen als Metadaten analysieren", "jobmeta_demo_state_v48", "topPublicExportButton", "GitHub-Paket erstellen", "Status und Notizen</th>"]:
            if obsolete == "Status und Notizen</th>":
                # This exact header is expected in the real dashboard shell.
                continue
            if obsolete in html:
                fail(f"{name} app still contains obsolete static demo marker: {obsolete}")

    shim = (ROOT / "static-api-shim.js").read_text(encoding="utf-8")
    for marker in ["/api/jobs", "/api/load-demo", "static-api-data.json", "jobmeta_static_demo_jobs_v56"]:
        if marker not in shim:
            fail(f"static API shim missing marker: {marker}")

    data = json.loads((ROOT / "data" / "static-api-data.json").read_text(encoding="utf-8"))
    if data.get("version") != "v56":
        fail("static demo data must be v56")
    if len(data.get("profiles", [])) != 3 or len(data.get("datasets", [])) != 3:
        fail("static demo data must contain three profiles and three datasets")
    scored = data.get("scored", {})
    for profile in ["information_management", "statistics", "it_support"]:
        if profile not in scored:
            fail(f"missing scored profile bundle: {profile}")
        for dataset in ["information_management", "statistics", "it_support"]:
            if len(scored[profile].get(dataset, {}).get("jobs", [])) < 20:
                fail(f"scored data for {profile}/{dataset} is unexpectedly small")

    service_worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
    for marker in ["jobmeta-demo-v56g", "./static-api-shim.js", "./data/static-api-data.json"]:
        if marker not in service_worker:
            fail(f"service worker missing marker: {marker}")

    print("PWA live demo files: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
