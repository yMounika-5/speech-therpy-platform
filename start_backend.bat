@echo off
echo ========================================
echo   Starting Speech Therapy Backend
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call backend_venv\Scripts\activate.bat

echo.
echo Starting FastAPI server...
echo Server will be available at: http://127.0.0.1:8000
echo API Documentation: http://127.0.0.1:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

uvicorn app.main:app --reload
