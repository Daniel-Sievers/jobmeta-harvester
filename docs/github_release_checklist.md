# GitHub Release Checklist

Diese Checkliste hilft vor dem Veröffentlichen des Projekts.

## Vor dem Commit

- [ ] Keine echte `data/jobs.sqlite` committen.
- [ ] Keine echten CV-Dateien committen.
- [ ] Keine privaten Bewerbungsnotizen committen.
- [ ] Keine Screenshots mit echten Stellenlisten oder privaten Browserdaten.
- [ ] `python -m unittest discover tests` ausführen.
- [ ] Public-Export erzeugen:

```bash
python -m jobmeta_harvester --prepare-github-release
```

## README prüfen

- [ ] Projektidee ist in den ersten Absätzen klar.
- [ ] Screenshots sind neutral.
- [ ] Setup-Anleitung funktioniert.
- [ ] Demo-Modus ist erklärt.
- [ ] Grenzen zu Scraping und Plattformen sind erklärt.
- [ ] Datenschutz-/Public-Export-Hinweis ist sichtbar.

## Demo prüfen

- [ ] Dashboard startet lokal.
- [ ] `Demo starten` öffnet das Demo-Fenster.
- [ ] Drei Demo-Profile sind auswählbar.
- [ ] Drei Demo-Datensätze sind auswählbar.
- [ ] Demo laden zeigt Jobs im Dashboard.
- [ ] Detailansicht und Speichern funktionieren.
- [ ] Public-Export kann über Button erzeugt werden.

## Optional für Portfolio

- [ ] Demo-GIF aufnehmen.
- [ ] GitHub Pages für statische Demo-Landingpage einrichten.
- [ ] Repository-Beschreibung ergänzen.
- [ ] Topics setzen, z. B. `python`, `sqlite`, `csv`, `metadata`, `information-management`.

## Nicht vergessen

Das öffentliche Repository soll das Projekt zeigen, nicht private Bewerbungsdaten.
Für echte Nutzung lokal arbeiten; für GitHub den Public-Export verwenden.
