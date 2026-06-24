# Version 51 - PWA final cleanup

This version is the final cleanup after unifying the static PWA and the local dashboard shell.

## Changed

- Removed obsolete hand-built demo frontend leftovers:
  - `app.js`
  - `demo/app.js`
  - `demo/app.css`
  - `demo/manifest.webmanifest`
  - `demo/service-worker.js`
  - `demo/version.json`
  - `demo/offline.html`
  - `data/demo-data.json`
  - `demo/data/demo-data.json`
  - duplicated `demo/assets/`
- Kept a single dashboard shell for `/app/` and `/demo/`.
- Kept `/demo/` as the forced demo route and `/app/` as the tool route.
- Updated cache/version markers to `v51`.
- Updated automated checks so removed legacy files cannot re-enter the public package unnoticed.

## Result

The public package now follows the intended structure:

- `/` = mode selector
- `/app/` = tool mode
- `/demo/` = demo mode with required demo selection
- no separate visual demo app
