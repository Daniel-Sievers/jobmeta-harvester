@echo off
setlocal

set PY_CMD=

py -3 --version >nul 2>nul
if %errorlevel%==0 set PY_CMD=py -3

if "%PY_CMD%"=="" (
  python --version >nul 2>nul
  if %errorlevel%==0 set PY_CMD=python
)

if "%PY_CMD%"=="" (
  python3 --version >nul 2>nul
  if %errorlevel%==0 set PY_CMD=python3
)

if "%PY_CMD%"=="" (
  echo Python wurde nicht gefunden.
  echo Installiere Python 3 und aktiviere bei der Installation "Add python.exe to PATH".
  echo Danach dieses Fenster schliessen und start_dashboard_windows.bat erneut starten.
  pause
  exit /b 1
)

echo Verwende: %PY_CMD%
echo Erzeuge lokale Demo-Daten...
%PY_CMD% -m src.jobmeta_harvester --sample
if errorlevel 1 (
  echo Demo-Daten konnten nicht erzeugt werden.
  pause
  exit /b 1
)

echo.
echo Dashboard startet lokal unter:
echo http://127.0.0.1:8765
echo.
%PY_CMD% -m src.jobmeta_harvester --dashboard

pause
