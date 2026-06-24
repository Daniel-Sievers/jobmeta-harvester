# Deployment und Live-Demo

JobMeta Harvester besteht aus zwei Teilen:

1. **Lokale Vollversion**: Python-Dashboard mit SQLite, CSV-Import und CV-Import.
2. **Öffentliche PWA-Demo**: statische, installierbare Demo mit neutralen Profilen und Recherche-Snapshot-Daten.

Die öffentliche Live-Demo öffnet direkt die Dashboard-Oberfläche und zeigt zuerst das Demo-Datenfenster. Besucher:innen wählen einen Demo-Lebenslauf und einen Recherche-Snapshot, laden die Demo und können danach Scores, Skill-Lücken, Quellen und Details ausprobieren.

## Warum nicht die gesamte lokale App deployen?

Die Vollversion speichert private Bewerbungsdaten lokal in SQLite. Für ein öffentliches Portfolio ist das ein Vorteil: echte Daten bleiben lokal. Die Live-Demo verwendet deshalb nur neutrale Demo-Daten im Browser.

## Empfohlenes Deployment

- GitHub-Repo mit der Public-Version veröffentlichen.
- Vercel mit dem Repo verbinden.
- Für die öffentliche Demo den Link `/demo/` verwenden; die Startauswahl zeigt eine Auswahl und `/app/` öffnet den Werkzeugmodus.

Beispiel:

```text
https://<dein-projekt>.vercel.app/
```

`/demo/` bleibt als Kompatibilitätsroute bestehen, ist aber nicht der Hauptlink.
