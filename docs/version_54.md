# Version 54 – Scrollleiste und Bedienleiste bereinigt

Version 54 räumt zwei sichtbare UX-Punkte auf, die in der Demo und im Werkzeugmodus irritiert haben.

## Änderungen

- Der Button **GitHub-Paket erstellen** wurde aus der normalen Dashboard-Buttonleiste entfernt.
- Der Public-Export bleibt als Kommandozeilen-/Entwicklerfunktion dokumentiert:

```bash
python -m jobmeta_harvester --prepare-github-release
```

- Die doppelte horizontale Tabellenbedienung wurde bereinigt:
  - die native horizontale Scrollleiste direkt an der Tabelle wird ausgeblendet,
  - die feste Scrollleiste am unteren Fensterrand bleibt als einzige sichtbare horizontale Tabellensteuerung,
  - die Leiste hat jetzt einen undurchlässigen Hintergrund,
  - sie ist höher und damit leichter mit der Maus zu greifen,
  - der Hauptbereich hat mehr unteren Abstand, damit die Leiste keine Inhalte verdeckt.

## Routen

- `/` – Startauswahl
- `/app/` – Werkzeugmodus
- `/demo/` – Demo-Modus mit verpflichtender Demo-Auswahl
- `/local/` – Erklärung der lokalen Python-/SQLite-Version

## Ergebnis

Die Oberfläche wirkt ruhiger: weniger Entwicklerfunktionen in der normalen Bedienleiste und nur eine klare horizontale Tabellen-Scrollsteuerung.
