$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "EvalBench launcher — first run may take a few minutes." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root\backend'; if (!(Test-Path '.venv')) { python -m venv .venv }; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt; if (!(Test-Path '.env')) { Copy-Item .env.example .env }; python seed.py; uvicorn app.main:app --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$root\frontend'; npm install; npm run dev"
Write-Host "Backend and frontend terminals opened. Visit http://localhost:5173 after startup." -ForegroundColor Green
