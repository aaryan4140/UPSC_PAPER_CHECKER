@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo        UPSC Answer Evaluator
echo ================================================
echo.

:: Find Python
set "PYTHON_CMD=python"
where py >nul 2>nul
if not errorlevel 1 ( set "PYTHON_CMD=py -3" )

%PYTHON_CMD% --version >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Download Python from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found.

:: Create venv if not exists
if not exist "venv" (
    echo.
    echo [SETUP] First time setup - creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created.

    :: Install dependencies
    echo.
    echo [SETUP] Installing dependencies (2-3 minutes)...
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed.
) else (
    call venv\Scripts\activate.bat
)

:: Check .env
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
    )
    echo.
    echo ================================================
    echo [ACTION REQUIRED]
    echo Open the .env file and paste your GEMINI_API_KEY
    echo Then run this file again.
    echo ================================================
    echo.
    pause
    exit /b 0
)

:: Launch
echo.
echo Launching app... Browser will open shortly.
echo (Press Ctrl+C here to stop the app)
echo.
streamlit run app/main.py

pause
endlocal
