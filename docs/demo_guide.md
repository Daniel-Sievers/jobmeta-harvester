# Demo-Guide

Dieser Guide beschreibt einen sicheren Demo-Ablauf mit neutralen Beispieldaten.
Er ist für GitHub, Bewerbungen und kurze Projektvorstellungen gedacht.

## Ziel der Demo

In 2 bis 4 Minuten soll sichtbar werden:

- JobMeta Harvester sammelt und strukturiert Stellenanzeigen.
- Das Dashboard hilft beim Filtern, Bewerten und Notieren.
- Skill-Lücken werden nicht nur gesammelt, sondern eingeordnet.
- Private Daten können durch den Public-Export geschützt werden.

## Neuer Demo-Modus im Dashboard

Im Dashboard gibt es den Button:

```text
Demo-Daten laden
```

Das Demo-Fenster hat zwei Spalten:

- links: Demo-Lebenslauf auswählen
- rechts: Demo-Jobdatensatz auswählen

Verfügbare Demo-Profile:

- Informationsmanagement
- Statistik / Datenanalyse
- IT / Support / Dokumentation

Verfügbare Demo-Datensätze:

- Informationsmanagement-Snapshot
- Statistik-/Analyse-Snapshot
- IT-/Support-Snapshot

Die Snapshot-Datensätze liegen unter:

```text
examples/research_snapshots/
```

Sie wurden am 19.06.2026 als kuratierte CSV-Snapshots angelegt. Einige Links
können veralten oder auf Such-/Listenansichten zeigen.

Die Option `vorherige Demo-Jobs entfernen` löscht nur Demo-Quellen wie
`sample`, `demo`, `demo-it` oder `demo-stat`. Manuell importierte Arbeitsdaten
bleiben erhalten.

## Vorbereitung

Projekt installieren oder direkt aus dem Repository starten:

```bash
python -m pip install -e .
```

Demo-Daten erzeugen:

```bash
python -m jobmeta_harvester --sample
```

Dashboard starten:

```bash
python -m jobmeta_harvester --dashboard
```

Ohne Installation geht auch:

```bash
python -m src.jobmeta_harvester --sample
python -m src.jobmeta_harvester --dashboard
```

Dann öffnen:

```text
http://127.0.0.1:8765
```

## Optional: reichhaltige Demo-CSV importieren

Für eine aussagekräftigere Demo liegt eine JobMeta-CSV bereit:

```text
examples/demo_jobmeta_import.csv
```

Für eine stärker IT-nahe Demo gibt es zusätzlich:

```text
examples/demo_it_jobs.csv
```

Im Dashboard:

1. `CSV importieren` klicken.
2. `examples/demo_jobmeta_import.csv` oder `examples/demo_it_jobs.csv` auswählen.
3. Nach Score, Priorität oder Quelle filtern.
4. Einen Job über `Details` öffnen.

## Optional: Demo-Lebenslauf laden

Für den CV-Import liegt ein fiktiver IT-/Informationsmanagement-Lebenslauf vor:

```text
examples/demo_cv_it_profile.txt
```

Als zweiter Testfall liegt ein Statistik-/Datenanalyse-Lebenslauf vor:

```text
examples/demo_cv_statistics_profile.txt
```

Im Dashboard:

1. `Profil aus CV laden` klicken.
2. Einen der Demo-Lebensläufe auswählen.
3. Warten, bis die Benachrichtigung `Profil aktualisiert ...` erscheint.
4. Danach werden vorhandene Jobs neu bewertet.

Der Demo-CV enthält bewusst Begriffe wie:

- Documentation / Dokumentation
- Knowledge Base / Wissensmanagement
- Data Quality / Datenqualität
- SQL, Python, CSV, JSON
- GitHub, Linux, Markdown

Dadurch kann man zeigen, wie aus CV-Text ein lokales Matching-Profil entsteht.

Der Statistik-CV enthält bewusst andere Schwerpunkte:

- Statistik / statistics
- quantitative analysis / quantitative Methoden
- Datenanalyse / data analysis
- Reporting
- Power BI
- SPSS
- RStudio

So kann man testen, ob sich die Profil-JSON und die Jobbewertung sichtbar
verändern.

Zusätzlich gibt es einen Informationsmanagement-CV:

```text
examples/demo_cv_information_management.txt
```

## Demo-Ablauf

### 1. Überblick zeigen

Zeige:

- Gesamtzahl der Jobs
- Score 70+
- Remote
- Nächste Schritte
- Lernpriorität

Erklärung:

> Das Dashboard behandelt Stellenanzeigen wie Metadatensätze. Es zeigt nicht nur
> Titel und Firma, sondern auch Matching, Skill-Lücken und Bewerbungsworkflow.

### 2. Filtern

Filtere nach:

- Mindestscore `70+`
- Priorität `hoch`
- Ansicht `Analyse`

Erklärung:

> So kann ich zuerst die Stellen ansehen, die fachlich und praktisch am ehesten
> passen.

### 2b. CV-Import zeigen

Lade den Demo-Lebenslauf:

```text
examples/demo_cv_it_profile.txt
```

Oder zum Vergleich:

```text
examples/demo_cv_statistics_profile.txt
```

Erklärung:

> Das Profil wird aus einem CV-Text aktualisiert. Danach werden die vorhandenen
> Stellen neu bewertet. In einer echten Nutzung würde man das Ergebnis manuell
> prüfen und bei Bedarf im Profil-JSON nachschärfen.

### 3. Details öffnen

Öffne eine passende Demo-Stelle, z. B.:

- `Junior Knowledge Management Specialist`
- `Data Quality Analyst`
- `Metadata and Taxonomy Assistant`

Zeige:

- Ort / Remote / Start
- Erfahrung
- Hauptaufgaben
- Tools / Systeme
- Muss-Skills
- Lücken A/B/C
- Matching
- nächste Aktion
- Notiz

### 4. Speichern

Trage eine neutrale Notiz ein:

```text
Demo: CV auf Dokumentation und Datenqualität zuschneiden.
```

Klicke auf Speichern und zeige die Benachrichtigung.

### 5. Public-Export erklären

Der Public-Export ist keine normale Demo-Aktion mehr in der Oberfläche. Er bleibt
als Entwickler-/Kommandozeilenfunktion dokumentiert:

```bash
python -m jobmeta_harvester --prepare-github-release
```

Erklärung:

> Für GitHub wird eine bereinigte ZIP erzeugt. Lokale SQLite-Datenbank,
> private Notizen und persönliche Profilwerte werden nicht übernommen.

## Was nicht gezeigt werden sollte

- echte Bewerbungsnotizen
- echte CV-Dateien
- private Profilgewichtungen
- Browser-Tabs mit persönlichen Konten
- reale Stellenanzeigen, wenn Links oder Notizen privat sind

## Kurzer Demo-Satz für Bewerbungen

> JobMeta Harvester ist ein lokales Python-Projekt, das Stellenanzeigen in ein
> einheitliches Metadatenformat bringt, sie anhand eines Profils bewertet und
> einen strukturierten Bewerbungsworkflow mit CSV-Import, SQLite und Dashboard
> bereitstellt.
