@echo off
rem Inicia un servidor local (solo en este equipo) y abre el validador en el navegador.
rem Requiere Python 3. Si no lo tiene, abra index.html con doble clic en Chrome o Edge.
chcp 65001 >nul
cd /d "%~dp0"
set PUERTO=8765
where py >nul 2>nul
if %errorlevel%==0 (
  echo Servidor local en http://127.0.0.1:%PUERTO%/index.html  ^(cierre esta ventana para detenerlo^)
  start "" cmd /c "timeout /t 2 >nul & start http://127.0.0.1:%PUERTO%/index.html"
  py -m http.server %PUERTO% --bind 127.0.0.1
  goto fin
)
where python >nul 2>nul
if %errorlevel%==0 (
  echo Servidor local en http://127.0.0.1:%PUERTO%/index.html  ^(cierre esta ventana para detenerlo^)
  start "" cmd /c "timeout /t 2 >nul & start http://127.0.0.1:%PUERTO%/index.html"
  python -m http.server %PUERTO% --bind 127.0.0.1
  goto fin
)
echo No se encontro Python. Abra index.html con doble clic ^(funciona sin servidor en Chrome o Edge^).
pause
:fin
