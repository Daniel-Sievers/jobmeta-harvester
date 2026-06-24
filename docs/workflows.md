# Workflows und Quellenlogik

JobMeta Harvester kombiniert drei Wege, Stellenanzeigen in ein gemeinsames
Metadatenformat zu bringen.

## 1. API-Abruf

Geeignet für:

- schnelle Demo
- erlaubte Quellen
- wiederholbare Suchläufe
- technische Portfolio-Demonstration

Aktuell unterstützt:

- Arbeitnow
- Remotive

Vorteil:

- automatisierbar
- reproduzierbar
- sauberer als Scraping gegen Plattformregeln

Grenze:

- nicht jede relevante Stelle liegt in diesen APIs
- manche Anzeigen haben wenige Metadaten

## 2. CSV-Import

Geeignet für:

- manuelle Recherche
- ChatGPT-gestützte Recherche
- Excel-Listen
- Portale, die nicht direkt automatisiert werden sollen

Die CSV wird in das JobMeta-Format gebracht und dann genauso behandelt wie
API-Daten:

- Scoring
- Deduplikation
- Speicherung in SQLite
- Bearbeitung im Dashboard
- Export

Das ist der wichtigste hybride Weg: Recherche kann extern/manuell erfolgen,
aber die Auswertung passiert strukturiert im Tool.

## 3. Manueller Paste-Import

Geeignet für:

- einzelne interessante Anzeigen
- schnelle Erfassung aus dem Browser
- Nachtragen von Jobs ohne saubere CSV

Der Text wird grob analysiert und in Felder vorbereitet. Danach kann der
Datensatz im Dashboard korrigiert und gespeichert werden.

## Warum kein Login-Scraping?

Direktes Scraping großer Jobplattformen kann gegen Nutzungsbedingungen
verstoßen, ist technisch fragil und für ein Portfolio-Projekt schwer sauber zu
begründen.

Dieses Projekt setzt deshalb auf:

- erlaubte APIs
- CSV-Import
- manuelle Ergänzung
- klare Dokumentation der Grenzen

So bleibt der Fokus auf Informationsmanagement und Datenqualität statt auf dem
Umgehen von Plattformschutz.

## Webrecherche-Snapshots statt Plattform-Crawling

Für große Plattformen wie LinkedIn, StepStone, Indeed oder XING ist im Projekt
kein automatischer Crawler vorgesehen. Stattdessen können Suchergebnisse oder
Stellenanzeigen manuell oder KI-gestützt recherchiert, gekürzt/paraphrasiert und
als CSV-Snapshot in das JobMeta-Format übertragen werden.

Ein CSV-Snapshot ist:

- ein kuratierter Metadaten-Auszug
- zeitlich dokumentiert
- tabellentauglich gekürzt
- nicht als vollständige Kopie einer Stellenanzeige gedacht
- nicht Teil eines automatisierten Plattform-Scrapers

Diese Unterscheidung ist wichtig: Der Aufwand ähnelt manchmal einer Recherche,
aber das Tool selbst crawlt keine großen Plattformen und nutzt keine Login- oder
Anti-Bot-Umgehung.

## CSV-Prompt für externe Recherche

Das Dashboard enthält einen bearbeitbaren Prompt, der eine CSV im JobMeta-Format
anfordert. Wichtig ist dabei:

- direkte Anzeigenlinks statt Suchergebnislinks
- leere Felder für `next_action` und `notes`
- kurze, tabellentaugliche Inhalte
- klare Unterscheidung von:
  - `gap_blocking`
  - `gap_learnable`
  - `gap_bonus`

## Empfohlener Bewerbungsworkflow

1. Suchbegriff festlegen.
2. Jobs über erlaubte APIs abrufen.
3. Für große Plattformen CSV über manuelle oder ChatGPT-gestützte Recherche
   vorbereiten.
4. CSV importieren.
5. Dubletten und Direktlinks prüfen.
6. Jobs mit hohem Score zuerst ansehen.
7. In den Details Notizen, Frist, Priorität und nächste Aktion pflegen.
8. CSV exportieren oder direkt aus dem Dashboard weiterarbeiten.

## Datenverantwortung

Die lokale Datenbank ist Arbeitsmaterial. Für Veröffentlichung, Screenshots und
GitHub sollte immer mit Demo-Daten oder dem Public-Export gearbeitet werden.
