# Projektstory: Warum JobMeta Harvester?

JobMeta Harvester ist aus einem praktischen Problem entstanden: Die Jobsuche
erzeugt viele verstreute Informationen. Anzeigen liegen auf verschiedenen
Portalen, Anforderungen sind schwer vergleichbar, Links und Notizen landen in
separaten Dateien, und die eigentliche Frage geht schnell unter:

> Welche Stellen passen realistisch zu meinem Profil, und wo sind die
> wichtigsten Lücken?

Das Projekt übersetzt diese Situation in ein Informationsmanagement-Problem.
Stellenanzeigen werden nicht nur als Fließtext betrachtet, sondern als
Metadatensätze:

- Quelle
- Link
- Unternehmen
- Rolle
- Ort und Remote-Anteil
- Aufgaben
- Tools und Systeme
- Muss- und Kann-Anforderungen
- Skill-Lücken
- Bewerbungsstatus
- nächste Aktion

Dadurch wird aus einer unübersichtlichen Recherche ein strukturierter Workflow.

## Gestaltungsentscheidung

Das Tool bewirbt sich nicht automatisch und versendet keine Bewerbungen. Es
sammelt, strukturiert und bewertet Informationen. Die Entscheidung bleibt beim
Menschen.

Diese Grenze ist Absicht:

- weniger Risiko durch fehlerhafte Automatisierung
- bessere Nachvollziehbarkeit
- respektvollerer Umgang mit Plattformregeln
- passend für ein Portfolio-Projekt im Bereich Informationsmanagement

## Warum lokal?

Bewerbungsdaten sind persönlich. Deshalb läuft das Dashboard lokal und nutzt
eine lokale SQLite-Datenbank. Für GitHub gibt es einen separaten Public-Export,
der private Daten entfernt und ein neutrales Beispielprofil verwendet.

## Was das Projekt zeigen soll

Das Projekt soll zeigen, dass technische Werkzeuge nicht nur gebaut, sondern
auch strukturiert, dokumentiert und verantwortungsvoll eingesetzt werden können.

Besonders sichtbar werden:

- Python-Grundlagen
- CSV- und JSON-Verarbeitung
- lokale Datenhaltung mit SQLite
- einfache API-Adapter
- Datenmodellierung
- Matching-Logik
- Dashboard-UX
- Datenschutzbewusstsein
- Dokumentation eines realistischen Workflows

Kurz gesagt: JobMeta Harvester ist ein kleines Werkzeug für digitale Ordnung im
Bewerbungsprozess.
