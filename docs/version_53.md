# Version 53 – Demo-Start entsperrt nach Pflichtauswahl

Diese Version korrigiert den Demo-Modus der statischen Public-PWA.

## Änderungen

- `/demo/` öffnet weiterhin automatisch das Demo-Auswahlfenster.
- Vor der Auswahl ist die restliche Oberfläche bewusst gesperrt.
- Nach `Demo laden` wird die Sperre vollständig aufgehoben.
- Die Toolbar bleibt danach normal benutzbar:
  - Echte Jobs abrufen lädt in der statischen PWA Snapshot-Daten.
  - CSV importieren funktioniert im Browser.
  - Profil aus CV laden funktioniert browserbasiert für Textsignale.
  - Profil bearbeiten, Job hinzufügen, Prompt bearbeiten und CSV-Export bleiben klickbar.
- Der Demo-Lock nutzt nun eine eigene CSS-/JS-Klasse und entfernt zusätzlich `inert`/`aria-hidden` nach erfolgreichem Laden.
- Versionen, Cache-Namen und Prüfscripte wurden auf v53 aktualisiert.

## Zielzustand

Der Demo-Link zeigt zuerst eine verpflichtende Auswahl. Danach ist es dieselbe Oberfläche wie der Werkzeugmodus, nur mit geladenen Demo-Daten.
