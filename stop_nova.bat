@echo off
title Stop N.O.V.A. Background Assistant
cls
echo Stopping N.O.V.A. background voice process...
powershell -Command "Get-Process -Name pythonw -ErrorAction SilentlyContinue | Stop-Process -Force"
echo N.O.V.A. background process stopped.
pause
