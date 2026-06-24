# Browser-Erweiterung: JobMeta Clipper

`JobMeta Clipper` ist eine optionale Browser-Erweiterung fuer das lokale JobMeta-Dashboard. Sie ist als **WebExtension** aufgebaut und wird in zwei Paketen ausgeliefert:

- `jobmeta-clipper-chromium.zip` fuer Chrome, Brave, Edge und andere Chromium-basierte Browser
- `jobmeta-clipper-firefox.zip` fuer Firefox

Die Erweiterung ist ein Einzelseiten-Clipper: Sie liest die gerade geoeffnete Jobanzeige erst nach einem Klick aus, zeigt die erkannten Felder im Popup zur Kontrolle an und sendet den Datensatz an dein lokales Dashboard.

## Was die Erweiterung macht

- liest nach einem Klick die aktive Browserseite aus
- uebernimmt Titel, Unternehmen, URL, Ort/Remote und einen Beschreibungsauszug, soweit erkennbar
- nutzt strukturierte JobPosting-Daten, wenn die Seite sie bereitstellt, und faellt sonst auf heuristische Erkennung zurueck
- erkennt haeufige Quellen wie LinkedIn, StepStone, Indeed, XING, Remotive, Workday, Greenhouse, Lever und Ashby automatisch
- kann pruefen, ob das lokale Dashboard erreichbar ist
- zeigt die Felder im Popup zur Kontrolle an
- sendet den Datensatz an das lokale Dashboard unter `http://127.0.0.1:8765/api/manual-job`
- legt den Job wie einen normal manuell eingetragenen Datensatz in SQLite ab

Die Erweiterung bewirbt sich nicht automatisch, crawlt keine Plattformen und ruft keine Listen massenhaft ab. Sie ist kein Scraper, sondern ein manueller Clipper fuer einzelne geoeffnete Anzeigen.


## Workflow als Demo

Für GitHub und Bewerbungen ist der Clipper besonders gut als kurzer Workflow erklärbar:

1. einzelne Stellenanzeige öffnen
2. Clipper starten
3. `Seite auslesen` klicken
4. Felder prüfen
5. `An JobMeta senden` klicken
6. Job im Dashboard bewerten und Notiz ergänzen

Eine kompakte Darstellung mit Mockup liegt hier:

```text
docs/browser_extension_workflow.md
```

## Voraussetzung

Vor der Nutzung muss das Dashboard lokal laufen:

```powershell
python -m jobmeta_harvester --dashboard
```

Danach muss im Browser erreichbar sein:

```text
http://127.0.0.1:8765
```

## Installation in Chrome, Brave oder Edge

1. Erweiterungsseite oeffnen:
   - Chrome: `chrome://extensions`
   - Brave: `brave://extensions`
   - Edge: `edge://extensions`
2. Entwicklermodus aktivieren.
3. `Entpackte Erweiterung laden` auswaehlen.
4. Diesen Ordner waehlen:

```text
browser_extension/jobmeta-clipper
```

Alternativ kann fuer Releases das Chromium-Paket genutzt werden:

```text
dist/browser_extension/jobmeta-clipper-chromium.zip
```

## Installation in Firefox

Fuer einen lokalen Test:

1. `about:debugging#/runtime/this-firefox` oeffnen.
2. `Temporary Add-on laden...` auswaehlen.
3. Die Firefox-Manifestdatei verwenden:

```text
browser_extension/jobmeta-clipper/manifest.firefox.json
```

Wenn Firefox eine Datei namens `manifest.json` erwartet, nutze das gebaute Firefox-ZIP:

```text
dist/browser_extension/jobmeta-clipper-firefox.zip
```

Das Firefox-ZIP enthaelt dieselben Popup-Dateien, aber eine Firefox-kompatible `manifest.json` mit `browser_specific_settings`.

## Pakete bauen

```powershell
python browser_extension/build_extension_packages.py
```

Erzeugt:

```text
dist/browser_extension/jobmeta-clipper-chromium.zip
dist/browser_extension/jobmeta-clipper-firefox.zip
```

## Nutzung

1. Dashboard lokal starten.
2. Eine Jobanzeige im Browser oeffnen.
3. Auf das JobMeta-Clipper-Icon klicken.
4. Optional `Dashboard pruefen` klicken, wenn du unsicher bist, ob JobMeta lokal laeuft.
5. `Seite auslesen` klicken.
6. Felder kurz pruefen oder korrigieren.
7. `An JobMeta senden` klicken.
8. Im Dashboard erscheint der Job in der Liste.

## Berechtigungen

Die Erweiterung nutzt Manifest V3 und moeglichst kleine Berechtigungen:

- `activeTab`: Zugriff nur auf den gerade aktiven Tab nach Benutzeraktion
- `scripting`: liest die aktuelle Seite nach Klick aus
- `tabs`: liest Tab-Titel und URL fuer die Vorbefuellung
- `storage`: merkt sich die lokale Dashboard-URL
- `host_permissions`: erlaubt Kommunikation mit `127.0.0.1:8765` und `localhost:8765`

## Grenzen

Die Extraktion nutzt zuerst strukturierte `JobPosting`-Daten, wenn eine Seite diese bereitstellt. Falls nicht, nutzt sie heuristische CSS-/Text-Erkennung. Jobportale verwenden unterschiedliche HTML-Strukturen; deshalb werden Titel, Unternehmen oder Ort nicht immer perfekt erkannt. Das Popup ist bewusst editierbar, damit der Datensatz vor dem Senden korrigiert werden kann.

Bei Seiten mit Login, starker Dynamik oder sehr restriktivem JavaScript kann die Extraktion unvollstaendig sein. Das ist erwartbar und kein Fehler des Datenmodells.

## Kompatibilitaet

- Chrome/Brave/Edge: nutzen das Chromium-Paket bzw. den Standardordner.
- Firefox: nutzt das Firefox-Paket bzw. `manifest.firefox.json`.
- Safari: nicht vorbereitet. Safari-Erweiterungen brauchen einen eigenen Packaging-/Signierungsweg.
