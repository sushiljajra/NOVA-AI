@echo off
title Install N.O.V.A. Auto-Startup
cls
echo ========================================================
echo   N.O.V.A. Auto-Start Installer
echo ========================================================
echo.
echo Installing N.O.V.A. into Windows Startup folder...
echo This ensures N.O.V.A. is ALWAYS listening for "Nova"
echo automatically as soon as your laptop turns on!
echo.

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "TARGET_VBS=%STARTUP_FOLDER%\NOVA_Assistant.vbs"

echo Set WshShell = CreateObject("WScript.Shell") > "%TARGET_VBS%"
echo WshShell.CurrentDirectory = "D:\Projects\Eclipse" >> "%TARGET_VBS%"
echo WshShell.Run """D:\Projects\Eclipse\.venv\Scripts\pythonw.exe"" run_nova.py --wake", 0, False >> "%TARGET_VBS%"

echo.
echo [SUCCESS] N.O.V.A. has been installed into your Windows Startup!
echo File created: "%TARGET_VBS%"
echo.
echo Starting N.O.V.A. in the background now...
cscript //nologo "%TARGET_VBS%"
echo.
echo N.O.V.A. is now actively listening in the background!
echo Just say "Nova" or "Hey Nova" anytime!
echo ========================================================
pause
