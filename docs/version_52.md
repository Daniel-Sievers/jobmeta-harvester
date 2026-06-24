# Version 52 - PWA-Startseite und statische Demo-Aktionen

Diese Version verbessert die öffentliche PWA nach dem v51-Aufräumen.

## Geändert

- Die Root-Seite erklärt jetzt klarer die drei Einstiege: Demo, Werkzeugmodus und lokale Vollversion.
- Die lokale Vollversion hat eine eigene kleine Infoseite unter `/local/`, statt nur auf die rohe README-Datei zu verweisen.
- Die statische PWA kann nun mehr Aktionen im Browser ausführen:
  - CSV-Dateien importieren
  - manuelle Jobs anlegen
  - Profil-JSON bearbeiten
  - Text-CVs grob auswerten
  - Snapshot-Daten über den Abruf-Button laden
- Aktionen, die wirklich Backend-Zugriff brauchen, melden klar, dass die lokale Vollversion nötig ist.
- Versionen und Service-Worker-Cache wurden auf v52 aktualisiert.

## Zweck

Die Demo soll nicht wie ein funktionsloses Bild wirken. Nach der verpflichtenden Demo-Auswahl können Besucher:innen die Oberfläche aktiv ausprobieren, ohne dass private Daten oder ein Python-Backend nötig sind.
