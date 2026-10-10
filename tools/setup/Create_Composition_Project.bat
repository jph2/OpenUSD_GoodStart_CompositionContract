@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Create_Composition_Project.ps1" %*
set "CC_SETUP_EXIT=%ERRORLEVEL%"
echo.
pause
exit /b %CC_SETUP_EXIT%
