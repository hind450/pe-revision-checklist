@echo off
echo ==========================================
echo PE Assessment System - Web Interface
echo ==========================================
echo.
echo Starting web server...
echo.

cd /d "%~dp0\web"
python app.py
pause
