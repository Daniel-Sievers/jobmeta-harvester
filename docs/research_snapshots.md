# Recherche-Snapshots

JobMeta Harvester nutzt fuer die Demo sogenannte Recherche-Snapshots: CSV-Dateien mit strukturierten Job-Metadaten, die aus einer kuratierten Webrecherche entstanden sind.

## Was ist ein Recherche-Snapshot?

Ein Snapshot ist eine tabellarische Momentaufnahme: Suchbegriffe, sichtbare Trefferinformationen und einzelne oeffentlich erreichbare Stellen- oder Suchseiten werden in das JobMeta-Format uebertragen. Die Inhalte sind kurz, tabellentauglich und teilweise paraphrasiert.

## Was es nicht ist

Diese Snapshots sind **kein Login-Scraping**, kein Bot und kein automatisiertes Crawling grosser Jobplattformen. JobMeta ruft LinkedIn, StepStone, Indeed oder XING nicht massenhaft automatisiert ab. Bei solchen Plattformen ist der robuste Workflow: Webrecherche oder ChatGPT-gestuetzte Suche -> CSV-Snapshot -> Import ins lokale Dashboard.

## Warum dieser Weg?

- grosse Jobplattformen blockieren oder begrenzen automatisiertes Crawling,
- viele Treffer sind login-, orts- oder sessionabhaengig,
- direkte Links koennen veralten,
- fuer Portfolio- und Demo-Zwecke reicht eine nachvollziehbare Momentaufnahme,
- echte persoenliche Bewerbungsdaten bleiben lokal.

## Demo-Snapshots in diesem Projekt

Stand: 2026-06-21

- IT-Systemadministration / IT Support
- Metadaten / Informationsmanagement
- Statistik / Data Analysis

Jeder Datensatz enthaelt 12 strukturierte Treffer im JobMeta-CSV-Format. Einige Links sind direkte Anzeigenlinks, andere sind Such- oder Trefferseiten und entsprechend als Recherche-Snapshot zu verstehen.

## Nutzung im Dashboard

1. Dashboard starten.
2. `Demo-Daten laden` oeffnen.
3. Demo-Profil und Recherche-Snapshot waehlen.
4. Optional vorherige Demo-Jobs entfernen.
5. `Demo laden` klicken.

Die Daten werden lokal in die SQLite-Datenbank importiert und mit dem gewaehleten Demo-Profil bewertet.

## Erweiterte Snapshot-Datensätze (v38)

Die Demo-Datensätze wurden in v38 erweitert, damit die Live-Demo realistischer wirkt:

- Metadaten / Informationsmanagement: 36 Einträge
- Statistik / Data Analysis: 26 Einträge
- IT-Systemadministration / IT Support: 21 Einträge

Zusätzlich gibt es ein maschinenlesbares Manifest:



Die Datensätze sind kuratierte Recherche-Snapshots. Sie basieren auf öffentlicher Websuche und sichtbaren Trefferseiten, nicht auf automatisiertem Crawling großer Jobplattformen. Einige Links können veralten oder auf Such-/Listenansichten zeigen.

