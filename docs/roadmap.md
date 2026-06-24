# Roadmap

Diese Roadmap beschreibt sinnvolle nächste Schritte. Sie ist bewusst in kleine
Pakete gegliedert, damit das Projekt als Portfolio-Projekt nachvollziehbar
weiterentwickelt werden kann.

## Aktueller Stand

- lokales Dashboard
- SQLite-Datenbank
- CSV-Import und CSV-Export
- API-Adapter für Arbeitnow und Remotive
- Profilbasiertes Scoring
- CV-basierte Profilaktualisierung
- Bewerbungsworkflow mit Status, Priorität, Frist und Notizen
- Public-/GitHub-Export ohne private Daten
- Tests für Kernlogik und Public-Export

## Als Nächstes

### 1. Demo-Reife

- kurze Demo-GIF oder Videoaufnahme
- klarer Demo-Ablauf im README
- bessere Demo-Daten mit mehreren Rollenclustern
- Screenshots aus Demo-Daten statt aus echten Bewerbungsdaten

### 2. Dokumentation abrunden

- GitHub-Repo-Beschreibung formulieren
- kurze „How to review this project“-Sektion
- Troubleshooting für Windows, Python-Versionen und Port-Konflikte

### 3. Matching transparenter machen

- Score-Komponenten im Dashboard anzeigen
- Gewichtung im Profil-Editor verständlicher erklären
- „Warum passt diese Stelle?“ kompakter darstellen

## Später denkbar

### Quellen erweitern

- weitere erlaubte APIs anbinden
- RSS-Feeds oder Jobseiten mit ausdrücklicher Erlaubnis auswerten
- Importprofile für verschiedene CSV-Formate

### UI verbessern

- gespeicherte Filteransichten
- Spaltenreihenfolge anpassbar machen
- kompakte Kartenansicht für schnelle Sichtung
- bessere mobile Darstellung

### Datenqualität

- Dublettenvergleich über Ähnlichkeit statt nur Job-Key
- Erkennung von Suchergebnislinks vs. Direktlinks weiter verbessern
- Plausibilitätschecks für Fristen und Remote-Angaben

### Export und Reporting

- Bewerbungsreport als Markdown oder HTML
- Skill-Gap-Bericht pro Suchlauf
- Lernplan aus wiederkehrenden Lücken ableiten

## Nicht geplant

- automatisches Abschicken von Bewerbungen
- Umgehen von Plattformregeln oder Login-Scraping
- zentrale Cloud-Datenbank mit persönlichen Bewerbungsdaten
- Speicherung echter CVs im öffentlichen Repository

Diese Grenzen sind Teil des Projektkonzepts. Das Tool soll Recherche und
Entscheidungen unterstützen, nicht Bewerbungshandlungen automatisieren.
