@echo off
setlocal
cd /d "%~dp0"

echo Starting UPSC Paper Evaluator...
echo.

set "PYTHON_CMD=python"
where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
)

where %PYTHON_CMD% >nul 2>nul
if errorlevel 1 (
    echo Python was not found on this system.
    echo Please install Python 3.10+ and make sure it is added to PATH.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Launching the app...
streamlit run app\main.py

if errorlevel 1 (
    echo.
    echo The app did not start successfully.
    pause
)

endlocal
