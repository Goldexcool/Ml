@echo off
echo ========================================
echo Starting Tomato Disease Classifier API
echo ========================================
echo.
echo Server will start at: http://localhost:8000
echo API Docs available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Activate virtual environment and start server
call .venv\Scripts\activate.bat
python -m uvicorn main:app --reload

pause
