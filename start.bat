@echo off
echo Starting UPSC Answer Evaluator...
echo.

cd /d "%~dp0"

:: Activate virtual environment
call venv\Scripts\activate.bat 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

:: Launch Streamlit
echo App is starting... Browser will open automatically.
echo (Press Ctrl+C in this window to stop the app)
echo.
streamlit run app/main.py
pause
