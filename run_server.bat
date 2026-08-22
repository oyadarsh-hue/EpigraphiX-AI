@echo off
title EpigraphiX-AI Web Studio Server
cd /d "%~dp0"
python serve.py
if errorlevel 1 (
    echo.
    echo [!] Failed to start using Python. Trying py launcher...
    py serve.py
)
pause
