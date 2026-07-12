@echo off
echo ============================================
echo    UPSC Answer Evaluator - Setup
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo [OK] Python found.
echo.

:: Create virtual environment
echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment created.
echo.

:: Activate and install dependencies
echo [2/4] Installing dependencies (this may take 2-3 minutes)...
call venv\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.
echo.

:: Install Poppler for PDF preview
echo [3/4] Checking Poppler (needed for PDF preview)...
where pdftoppm >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Poppler not found. PDF preview will not work.
    echo To install Poppler:
    echo   1. Download from: https://github.com/oschwartz10612/poppler-windows/releases
    echo   2. Extract the folder
    echo   3. Add the "bin" folder to your system PATH
    echo   4. Restart this setup
    echo.
    echo You can skip this - the tool will still work without PDF preview.
    echo.
) else (
    echo [OK] Poppler found.
)

:: Check .env file
echo [4/4] Checking configuration...
if not exist .env (
    copy .env.example .env >nul 2>&1
    echo [ACTION REQUIRED] .env file created.
    echo Please open .env and add your GEMINI_API_KEY.
) else (
    echo [OK] .env file exists.
)
echo.

echo ============================================
echo    Setup Complete!
echo ============================================
echo.
echo Next steps:
echo   1. Open .env file and paste your GEMINI_API_KEY
echo   2. Double-click "start.bat" to launch the app
echo.
pause
