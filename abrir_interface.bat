@echo off
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (
  py -3 projeto_final\interface_grafica.py %*
) else (
  python projeto_final\interface_grafica.py %*
)
if errorlevel 1 (
  echo.
  echo Verifique se o Python 3.10 ou superior esta instalado com Tkinter.
  pause
)
