# Reviewer Guide

Dieser Guide ist für Personen gedacht, die das Repository im Bewerbungs- oder
Portfolio-Kontext schnell einschätzen möchten.

## Kurzfassung

JobMeta Harvester ist ein lokales Python-Projekt für strukturierte Jobsuche.
Es sammelt oder importiert Stellenanzeigen, normalisiert sie als Metadaten,
bewertet sie anhand eines Profils und stellt sie in einem Browser-Dashboard dar.

## Schnell prüfen

```bash
python -m pip install -e .
python -m unittest discover tests
python -m jobmeta_harvester --dashboard
```

Dann öffnen:

```text
http://127.0.0.1:8765
```

Im Dashboard:

1. `Demo starten` klicken.
2. Demo-Lebenslauf und Demo-Jobdatensatz wählen.
3. `Demo laden` klicken.
4. Filter, Details und Notizen ansehen.

## Was anschauen?

| Bereich | Warum relevant? |
|---|---|
| `src/jobmeta_harvester/database.py` | SQLite-Schema, Deduplikation, Import, Tracking-Felder |
| `src/jobmeta_harvester/dashboard.py` | lokales Dashboard, API-Endpunkte, Demo-Modus |
| `src/jobmeta_harvester/profile_builder.py` | CV-Text zu Matching-Profil |
| `src/jobmeta_harvester/public_export.py` | Datenschutzfreundlicher GitHub-Export |
| `tests/` | Unit Tests für Kernlogik, Demo-Daten und Public-Export |
| `docs/architecture.md` | Architektur und Datenfluss |
| `docs/research_snapshots.md` | Erklärung der CSV-Snapshots |

## Was das Projekt bewusst nicht macht

- keine automatischen Bewerbungen
- kein Login-Scraping
- kein automatisiertes Crawling großer Jobplattformen
- keine Cloud-Datenbank mit Bewerbungsdaten

## Datenschutzprüfung

Für ein öffentliches GitHub-Repo sollte die Public-ZIP genutzt werden:

```bash
python -m jobmeta_harvester --prepare-github-release
```

Der Export entfernt:

- SQLite-Datenbanken
- lokale Datenexporte
- Python-Cache-Dateien
- private Profilwerte

## Geeignete Bewertungsperspektive

Das Projekt soll nicht zeigen, dass hier ein vollständiges Recruiting-System
gebaut wurde. Es zeigt eher:

- Informationsstruktur
- Datenqualität
- Python-Grundlagen
- CSV/JSON/SQLite
- UI- und Workflow-Denken
- Dokumentation
- verantwortungsvoller Umgang mit Plattformgrenzen und privaten Daten
