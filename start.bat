@echo off
echo ========================================
echo   Audio Splitter Backend Server
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate venv
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Start server
echo.
echo ========================================
echo   Starting server on http://localhost:8000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
