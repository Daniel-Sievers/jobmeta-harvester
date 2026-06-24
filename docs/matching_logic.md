# Matching Logic

Der Scorer arbeitet absichtlich transparent und regelbasiert.

1. Starte mit `base_score` aus `config/profile.json`.
2. Suche positive Begriffe in Titel, Beschreibung, Ort und Tags.
3. Suche negative Begriffe in denselben Feldern.
4. Titel-Treffer zaehlen etwas staerker, weil der Stellentitel meist das beste Signal ist.
5. Bevorzugte Orte oder Remote-Hinweise geben Zusatzpunkte.
6. Der finale Score wird auf 0 bis 100 begrenzt.

Das ist keine KI-Bewertung. Gerade deshalb ist es gut fuer Version 1:

- gut nachvollziehbar
- einfach zu dokumentieren
- leicht anpassbar
- gut testbar

Spaetere Versionen koennen semantische Suche oder Embeddings ergaenzen, ohne die
einfache Grundlogik zu verlieren.
