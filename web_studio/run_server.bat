@echo off
echo Starting Malayalam OCR Web Studio Server on http://localhost:8080 ...
cd /d "%~dp0"
python -m http.server 8080 --bind 0.0.0.0
pause
