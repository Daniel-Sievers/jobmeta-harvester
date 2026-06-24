# Version 57d - README/Public-Output bereinigt

Dieses Reparatur-Update trennt die Repository-README sauber vom statischen
Vercel-Ausgabeordner.

- `public/README.md` wird entfernt.
- `scripts/build_static_public.py` kopiert die README nicht mehr in `public/`.
- Alte SVG-Screenshot-Links werden aus der README entfernt, falls sie noch
  vorhanden sind.
- Ein Test stellt sicher, dass keine doppelte README im `public/`-Ordner
  erzeugt wird.

Hintergrund: Die Haupt-README liegt im Repository-Wurzelordner und bindet
Screenshots aus `docs/assets/screenshots/` ein. Eine zweite README unter
`public/` führt auf GitHub zu gebrochenen relativen Bildpfaden und ist für den
Vercel-Deploy nicht nötig.
