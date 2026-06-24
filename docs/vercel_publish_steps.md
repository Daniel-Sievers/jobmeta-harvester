# Vercel Publish Steps

Diese Schritte veröffentlichen die installierbare PWA-Demo. Die lokale Python-/SQLite-App bleibt weiterhin lokal.

## 1. Public-Paket entpacken

Nutze die aktuelle Public-Version, z. B.:

```text
jobmeta-harvester-public-v51
```

## 2. Auf GitHub hochladen

Den Inhalt des entpackten Ordners als Repository veröffentlichen, nicht die ZIP-Datei selbst.

## 3. Vercel verbinden

- Vercel öffnen
- GitHub-Repository importieren
- Standard-Einstellungen übernehmen
- Deploy starten

## 4. Live-Demo prüfen

Nach dem Deployment diese URL öffnen:

```text
https://<dein-projekt>.vercel.app/
```

Erwartetes Verhalten:

- Dashboard-Stil erscheint.
- Demo-Datenfenster öffnet automatisch.
- Das Fenster kann vor dem Laden nicht geschlossen werden.
- Profil + Snapshot auswählen.
- **Demo laden** klicken.
- Dashboard zeigt Jobs, Scores und Details.

## 5. PWA-Installation prüfen

In Brave/Chrome/Edge sollte nach kurzer Zeit das Installieren-Symbol erscheinen. Falls nicht:

- Seite einmal neu laden
- HTTPS prüfen
- Browser-Cache leeren
- Manifest und Service Worker in den DevTools prüfen

## 6. README-Link ersetzen

Wenn der finale Link feststeht, im README den Platzhalter ersetzen:

```text
https://<dein-projekt>.vercel.app/
```
