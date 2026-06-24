# Data Model

Version 1 normalisiert jede Stellenanzeige in ein gemeinsames Job-Objekt.

| Field | Purpose |
| --- | --- |
| `source` | Name der Quelle, zum Beispiel `arbeitnow` oder `remotive` |
| `source_id` | ID oder stabiler Slug aus der Quelle |
| `title` | Stellentitel |
| `company` | Unternehmen |
| `location` | Ort oder Remote-Hinweis |
| `remote` | `true`, `false` oder leer, wenn unklar |
| `url` | Link zur Anzeige |
| `date_posted` | Veroeffentlichungsdatum, falls vorhanden |
| `description` | Beschreibung als Text |
| `tags` | Tags, Kategorien oder Jobtypen |

Der CSV-Export fuegt Bewerbungsfelder hinzu:

| Field | Purpose |
| --- | --- |
| `match_score` | Bewertung von 0 bis 100 |
| `match_reason` | kurze Begruendung |
| `keywords_found` | gefundene positive und negative Begriffe |
| `application_status` | manuell nutzbar, z. B. `interesting`, `applied`, `rejected` |
| `notes` | manuelle Notizen |

## Version 2: SQLite

Version 2 speichert die normalisierten Jobs in `data/jobs.sqlite`.

Der primaere Schluessel ist `job_key`. Er wird aus normalisiertem Titel,
Unternehmen und Ort gebildet. Dadurch werden wiederholt gefundene Anzeigen
nicht als neue Zeilen angelegt, sondern aktualisiert.

Zusaetzliche Datenbankfelder:

| Field | Purpose |
| --- | --- |
| `first_seen` | Zeitpunkt, zu dem die Anzeige zuerst gespeichert wurde |
| `last_seen` | Zeitpunkt, zu dem die Anzeige zuletzt im Suchlauf gesehen wurde |
| `seen_count` | Anzahl der Suchlaeufe, in denen die Anzeige vorkam |
| `application_status` | manueller Bewerbungsstatus |
| `notes` | manuelle Notizen |

`application_status` und `notes` werden bei neuen Suchlaeufen nicht
ueberschrieben. Das macht die Datenbank zum stabilen Kern fuer ein spaeteres
Dashboard.

## Version 3: Dashboard

Das Dashboard liest die Jobs aus derselben SQLite-Datenbank und aktualisiert nur
die manuellen Felder:

- `application_status`
- `notes`

Alle Felder aus dem Harvesting- und Matching-Prozess bleiben weiterhin in der
Datenbank. Dadurch kann das Dashboard jederzeit geschlossen und spaeter wieder
gestartet werden, ohne Daten zu verlieren.

## Version 4: Analysefelder

Version 4 ergaenzt Felder, die aus der manuellen Excel-Analyse entstanden sind:

| Field | Purpose |
| --- | --- |
| `role_cluster` | fachliche Rollengruppe |
| `location_remote_start` | Ort, Remote-/Hybrid-Hinweis, Startinfo |
| `industry` | Branche oder Kontext |
| `main_tasks` | Hauptaufgaben |
| `work_pattern` | Muster der Arbeit, z. B. Doku, Abstimmung, Datenpflege |
| `tools_systems` | genannte Tools und Systeme |
| `must_skills` | Muss-Anforderungen |
| `nice_to_have` | Kann- oder Bonusanforderungen |
| `already_have` | vorhandene passende Faehigkeiten |
| `gap_blocking` | potenziell blockierende Luecken |
| `gap_learnable` | schnell lernbare Luecken |
| `gap_bonus` | Entwicklungs- oder Bonusfelder |
| `experience_required` | Erfahrungsniveau |
| `entry_realistic` | Einschaetzung des Einstiegs |
| `growth_value` | Lern- und Entwicklungswert |
| `interest` | eigenes Interesse |
| `decision` | aktuelle Entscheidung |

## Version 5: Editierbare Detailfelder

Die Detailansicht kann folgende Felder direkt aktualisieren:

| Field | Purpose |
| --- | --- |
| `application_status` | Workflow-Status |
| `decision` | fachliche Entscheidung |
| `interest` | eigenes Interesse |
| `entry_realistic` | Einschaetzung des Einstiegs |
| `growth_value` | Lern- und Entwicklungswert |
| `notes` | freie Notiz |

## Version 6: Analysefelder

Die Auswertung nutzt vorhandene Felder, legt aber keine neue Tabelle an:

| Source Field | Auswertung |
| --- | --- |
| `gap_blocking` | haeufige blockierende Luecken |
| `gap_learnable` | schnell lernbare Luecken |
| `gap_bonus` | Bonus- und Entwicklungsfelder |
| `must_skills` | wiederkehrende Muss-Anforderungen |
| `tools_systems` | haeufig genannte Tools |
| `already_have` | wiederkehrende vorhandene Staerken |

Die Lernprioritaet wird aus `gap_learnable` und `must_skills` berechnet.

## Version 7: Manuelle Datensaetze

Manuell eingefuegte Jobs nutzen dieselben Felder wie CSV-Importe. Der
Anzeigentext wird als `description` gespeichert und fliesst in Matching und
Suche ein.

Pflicht fuer einen stabilen Datensatz:

- `title`
- `company`

Empfohlen:

- `source`
- `url`
- `location_remote_start`
- `main_tasks`
- `must_skills`
- `nice_to_have`
- `notes`

## Version 8: Bewerbungsworkflow

Version 8 ergaenzt Felder, die aus einer reinen Trefferliste eine aktive
Bewerbungsliste machen:

| Field | Purpose |
| --- | --- |
| `priority` | eigene Prioritaet, z. B. `hoch`, `mittel`, `niedrig` |
| `application_deadline` | Bewerbungsfrist im Format `YYYY-MM-DD`, falls bekannt |
| `next_action` | naechster konkreter Schritt, z. B. `Lebenslauf anpassen` |

Diese Felder sind direkt im Dashboard editierbar, werden beim CSV-Export
mitgeschrieben und koennen ueber CSV-Import wieder aktualisiert werden.

## Version 9: Naechste Schritte

Version 9 legt keine neue Tabelle an. Die neue Arbeitsansicht nutzt vorhandene
Workflow-Felder:

| Field | Nutzung in V9 |
| --- | --- |
| `priority` | hohe Prioritaet erscheint in den naechsten Schritten |
| `application_deadline` | Fristen werden als ueberfaellig, heute faellig oder diese Woche faellig erkannt |
| `next_action` | konkrete naechste Schritte erscheinen direkt oberhalb der Tabelle |
| `application_status` | `rejected` und `ignored` werden aus der Naechste-Schritte-Liste ausgeblendet |

Der Workflow-Filter kann die Tabelle auf `Naechste Aktion`, `Ueberfaellig`,
`Diese Woche` oder `Hohe Prio` reduzieren.
