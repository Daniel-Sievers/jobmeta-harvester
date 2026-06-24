# Windows Start

Wenn PowerShell bei `python3` meldet, dass Python nicht gefunden wurde, ist das
normal: Unter Windows heisst der Befehl oft `py -3` oder `python`.

## 1. Python pruefen

In PowerShell im Projektordner:

```powershell
py -3 --version
```

Falls das nicht geht:

```powershell
python --version
```

Falls beides nicht geht, ist Python nicht richtig installiert oder nicht im PATH.
Dann Python 3 installieren und bei der Installation `Add python.exe to PATH`
aktivieren.

## 2. Demo-Daten erzeugen

```powershell
py -3 -m src.jobmeta_harvester --sample
```

Falls `py -3` nicht funktioniert, stattdessen:

```powershell
python -m src.jobmeta_harvester --sample
```

## 3. Dashboard starten

```powershell
py -3 -m src.jobmeta_harvester --dashboard
```

Danach im Browser oeffnen:

```text
http://127.0.0.1:8765
```

## Komfortstart

Alternativ kann in PowerShell oder per Doppelklick gestartet werden:

```powershell
.\start_dashboard_windows.bat
```

Die Datei erzeugt zuerst Demo-Daten und startet danach das lokale Dashboard.
