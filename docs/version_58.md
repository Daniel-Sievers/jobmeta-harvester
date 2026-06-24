# Version 58 - Repository-Cleanup

Dieses Update bereinigt die Public-/Vercel-Struktur:

- `public/` ist nur noch Build-Ausgabe und wird nicht mehr versioniert.
- `README.md` wird nicht mehr nach `public/README.md` kopiert.
- `/demo/` im Vercel-Build wird direkt aus derselben Dashboard-Quelle wie `/app/` erzeugt.
- Alte Screenshot-Links auf geloeschte SVG-Mockups wurden aus der Browser-Extension-Dokumentation entfernt.
- Tests pruefen, dass die doppelte Public-README nicht wieder auftaucht.
