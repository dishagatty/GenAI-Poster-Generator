# PromptPoster AI - PowerShell Launcher
Set-Location -Path $PSScriptRoot

if (-not (Test-Path ".\venv\Scripts\streamlit.exe")) {
    Write-Host "Virtual environment not found! Please check .\venv directory." -ForegroundColor Red
    pause
    exit 1
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   Starting PromptPoster AI Studio..." -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

Start-Process "http://localhost:8501"
& ".\venv\Scripts\streamlit.exe" run app.py
