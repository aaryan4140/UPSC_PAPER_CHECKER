@echo off
:: Creates a desktop shortcut for UPSC Evaluator with the app icon

set "SCRIPT_DIR=%~dp0"
set "SHORTCUT=%USERPROFILE%\Desktop\UPSC Evaluator.lnk"
set "TARGET=%SCRIPT_DIR%start.bat"
set "ICON=%SCRIPT_DIR%app\assets\images\app_icon.ico"

powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%TARGET%'; $s.IconLocation = '%ICON%'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Description = 'UPSC Answer Evaluator'; $s.Save()"

if exist "%SHORTCUT%" (
    echo.
    echo ================================================
    echo   UPSC Evaluator shortcut created on Desktop!
    echo   Double-click it to launch the app.
    echo ================================================
) else (
    echo [ERROR] Could not create shortcut.
)
echo.
pause
