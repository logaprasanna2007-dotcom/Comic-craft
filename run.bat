@echo off
title ComicCraft AI Server
cd /d "%~dp0"
echo ===================================================
echo   Starting ComicCraft AI Local Server
echo   App URL: http://127.0.0.1:8000
echo   Swagger Docs: http://127.0.0.1:8000/docs
echo ===================================================
echo.
"%~dp0.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
