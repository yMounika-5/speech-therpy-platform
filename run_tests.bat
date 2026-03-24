@echo off
echo ========================================
echo   Running API Tests
echo ========================================
echo.

cd /d "%~dp0"

echo Activating virtual environment...
call backend_venv\Scripts\activate.bat

echo.
echo Running test suite...
echo.

python test_complete_flow.py

echo.
echo ========================================
echo   Tests Complete
echo ========================================
echo.
pause
