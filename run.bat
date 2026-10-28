@echo off
title PromptPoster AI - Launcher
echo ========================================================
echo Starting PromptPoster AI...
echo ========================================================
cd /d "%~dp0"

if not exist "venv\Scripts\streamlit.exe" (
    echo Error: Virtual environment not found! Please run setup first.
    pause
    exit /b 1
)

echo Opening PromptPoster AI in your browser...
start http://localhost:8501
.\venv\Scripts\streamlit.exe run app.py
pause
