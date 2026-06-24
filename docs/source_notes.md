# Source Notes

Version 1 nutzt oeffentliche API-Endpunkte statt unerlaubtem Scraping.

## Arbeitnow

Arbeitnow beschreibt seine Job Board API als freie API ohne API-Key. Die Daten
enthalten unter anderem einen `remote`-Hinweis, der fuer die Bewertung von
Remote- oder Home-Office-Passung genutzt werden kann.

Genutzter Endpoint:

```text
https://www.arbeitnow.com/api/job-board-api
```

## Remotive

Remotive stellt eine Public API fuer aktive Remote-Jobs bereit. Die Dokumentation
nennt unter anderem den Endpoint `https://remotive.com/api/remote-jobs` sowie
optionale Query-Parameter wie `search`, `category`, `company_name` und `limit`.

Genutzter Endpoint:

```text
https://remotive.com/api/remote-jobs
```

## Portfolio-Grenze

Das Projekt soll Stellenanzeigen finden, normalisieren und bewerten. Es soll
keine Bewerbungen automatisch abschicken und keine Plattformregeln umgehen.
