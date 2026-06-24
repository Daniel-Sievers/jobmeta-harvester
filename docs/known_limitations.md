# Bekannte Grenzen

JobMeta Harvester ist ein lokales Portfolio-/MVP-Projekt. Einige Grenzen sind
bewusst gesetzt, andere wären sinnvolle spätere Verbesserungen.

## Datenquellen

- Das Tool nutzt nur erlaubte API-Quellen und CSV-/manuelle Importe.
- Große Plattformen wie LinkedIn, StepStone oder Indeed werden nicht direkt
  automatisiert gescraped.
- Ergebnisse aus APIs können unvollständig, veraltet oder unterschiedlich
  detailliert sein.
- Manche Quellen liefern keine guten Angaben zu Gehalt, Frist oder Remote-Grad.

## Matching

- Das Scoring ist keyword-basiert und damit erklärbar, aber nicht semantisch
  perfekt.
- Synonyme, Ironie, komplexe Rollenprofile oder schlecht formulierte Anzeigen
  können falsch bewertet werden.
- Der Score ersetzt keine menschliche Entscheidung.
- CV-basierte Profilableitung ist eine Hilfsfunktion und sollte manuell geprüft
  werden.

## Datenqualität

- Deduplikation basiert auf stabilen Schlüsseln aus URL, Quelle oder
  normalisierten Jobdaten.
- Ähnliche, aber nicht identische Anzeigen können trotzdem doppelt auftauchen.
- Suchergebnislinks können erkannt werden, aber nicht in jedem Fall automatisch
  in Direktlinks umgewandelt werden.

## Dashboard

- Das Dashboard ist lokal und bewusst schlicht gebaut.
- Es gibt keine Benutzerkonten, Rechteverwaltung oder Mehrbenutzerfähigkeit.
- Die UI ist für Desktop-Nutzung optimiert.
- Sehr große Datenmengen können die Übersichtlichkeit und Performance
  beeinträchtigen.

## Sicherheit und Datenschutz

- Die lokale SQLite-Datei kann private Bewerbungsnotizen enthalten.
- Für GitHub sollte immer der Public-Export genutzt werden.
- Screenshots sollten nur mit Demo-Daten erstellt werden.
- Echte CV-Dateien gehören nicht ins Repository.

## Deployment

- GitHub Pages reicht nicht für die vollständige App, weil ein Python-Backend
  und SQLite benötigt werden.
- Eine öffentliche Live-Demo müsste mit Demo-Daten auf einem Python-fähigen
  Hosting-Dienst laufen.
- Für Bewerbungen ist zunächst eine lokale Demo mit Screenshots/GIF oft
  realistischer und sicherer.

## Bewusste Produktgrenze

Das Tool sammelt, strukturiert und bewertet Informationen. Es verschickt keine
Bewerbungen und automatisiert keine Login-Plattformen. Diese Grenze ist
fachlich und ethisch gewollt.
