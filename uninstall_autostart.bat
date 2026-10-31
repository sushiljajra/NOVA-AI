@echo off
title Uninstall N.O.V.A. Auto-Startup
cls
echo ========================================================
echo   N.O.V.A. Auto-Start Remover
echo ========================================================
echo.
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "TARGET_VBS=%STARTUP_FOLDER%\NOVA_Assistant.vbs"

if exist "%TARGET_VBS%" (
    del "%TARGET_VBS%"
    echo [SUCCESS] Removed N.O.V.A. from Windows Startup.
) else (
    echo N.O.V.A. was not found in your Windows Startup folder.
)

echo.
pause
