# Version 55 – Vercel-Deploy-Fix

Version 55 ergänzt einen expliziten statischen Build-Output für Vercel.

## Änderung

- Neuer Build-Schritt `scripts/build_static_public.py`.
- `npm run vercel-build` erzeugt jetzt einen Ordner `public/`.
- Vercel kann dadurch mit dem Standard-Output-Directory `public` deployen.
- Die statische Ausgabe enthält Root-Auswahl, `/app/`, `/demo/`, `/demo/check`, `/local/`, Manifest, Service Worker, Icons und Demo-Daten.

## Grund

Vercel erwartet bei statischen Projekten häufig ein Output-Verzeichnis wie `public`. Vorher lagen die PWA-Dateien direkt im Repository-Wurzelverzeichnis. Lokal funktionierte das, aber der Vercel-Build konnte mit der Meldung `No Output Directory named "public" found` abbrechen.
