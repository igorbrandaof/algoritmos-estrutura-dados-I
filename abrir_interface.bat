@echo off
cd /d "%~dp0"
py -3 projeto_final\interface_grafica.py
if errorlevel 1 (
  echo.
  echo Verifique se o Python 3.10 ou superior esta instalado com Tkinter.
  pause
)
