# Public Export Checklist

Generated package root: `jobmeta-harvester-v35-public`

This archive is intended for a public GitHub upload or portfolio review.

## Automatic cleanup

- [x] SQLite-Datenbanken wurden nicht in die Public-ZIP übernommen.
- [x] Python-Cache-Dateien wurden nicht in die Public-ZIP übernommen.
- [x] Lokale Rohdaten- und Exportordner wurden nicht übernommen.
- [x] config/profile.json wurde durch ein neutrales Beispielprofil ersetzt.
- [x] config/profile.example.json wurde als Vorlage ergänzt.
- [x] Beispieldaten aus examples/ bleiben für Demo und Tests erhalten.

## Manual review before publishing

- [ ] Review screenshots before adding them to the repository.
- [ ] Do not commit real CV files, private notes, or real application tracking data.
- [ ] Use demo data from `examples/` for screenshots and demos.
- [ ] Run `python -m unittest discover tests` before publishing.
