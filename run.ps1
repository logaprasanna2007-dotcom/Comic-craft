Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Starting ComicCraft AI Local Server" -ForegroundColor Yellow
Write-Host "  App URL: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "  Swagger Docs: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan
Set-Location -Path $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
