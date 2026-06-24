# Browser-Clipper-Workflow

Der Browser-Clipper ist die optionale Brücke zwischen einer einzelnen geöffneten Jobanzeige und dem lokalen JobMeta-Dashboard.

![Browser extension workflow](assets/screenshots/browser-extension-workflow.svg)

## Wofür ist der Clipper gedacht?

Der Clipper ist für den Fall gedacht, dass eine interessante Stelle im Browser offen ist und schnell in JobMeta übernommen werden soll.

Er ersetzt nicht die Jobsuche selbst und crawlt keine Plattformen. Er liest nur die **aktuell geöffnete Seite nach einer Nutzeraktion** aus, zeigt die erkannten Felder im Popup an und sendet den Datensatz an das lokal laufende Dashboard.

## Ablauf

1. Dashboard lokal starten.
2. Eine einzelne Stellenanzeige im Browser öffnen.
3. JobMeta-Clipper öffnen.
4. `Dashboard prüfen` klicken, wenn unklar ist, ob JobMeta lokal läuft.
5. `Seite auslesen` klicken.
6. Titel, Firma, URL, Ort und Beschreibung im Popup prüfen oder korrigieren.
7. `An JobMeta senden` klicken.
8. Job im Dashboard öffnen, Score und Skill-Lücken prüfen und eigene Notizen ergänzen.

## Warum das kein Plattform-Scraping ist

Der Clipper ruft keine Suchergebnisseiten massenhaft ab und navigiert nicht automatisch durch Jobportale. Er nutzt keine Login-Automatisierung und bewirbt sich nicht automatisch.

Stattdessen ist er ein manueller Einzelseiten-Clipper:

- eine aktuell geöffnete Seite
- ein Klick zum Auslesen
- ein prüfbares Formular
- ein Datensatz im lokalen Dashboard

Für große Jobplattformen wie LinkedIn, StepStone, Indeed oder XING ist das der bevorzugte Weg gegenüber automatisiertem Crawling. Größere Trefferlisten können weiterhin über kuratierte CSV-Snapshots importiert werden.

## Demo für GitHub oder Bewerbungen

Eine kurze Demo kann diesen Ablauf zeigen:

1. Dashboard mit Demo-Daten öffnen.
2. Eine neutrale Demo-Stellenanzeige oder Beispielseite im Browser öffnen.
3. Clipper öffnen und `Seite auslesen` klicken.
4. Felder korrigieren.
5. `An JobMeta senden` klicken.
6. Im Dashboard erscheint der Job und kann bewertet werden.

Für die Aufnahme sollten nur neutrale Demo-Daten verwendet werden. Keine echten privaten Jobs, CVs, Notizen oder Browserprofile im Bild zeigen.

## Grenzen

Die Erkennung ist abhängig von der geöffneten Seite. Viele Jobseiten stellen strukturierte `JobPosting`-Daten bereit, andere nicht. Wenn keine strukturierten Daten vorhanden sind, nutzt die Erweiterung heuristische Erkennung. Deshalb sind Korrekturen im Popup normal und bewusst vorgesehen.
