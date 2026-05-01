@echo off
REM ═══════════════════════════════════════════════════════════════
REM CozMoz Admin Setup - Batch Script
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo   CozMoz Admin Setup
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if running with admin privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Please run as Administrator
    pause
    exit /b 1
)

REM Get the directory where this script is located
cd /d "%~dp0"

echo [1] Starting Python simple HTTP server...
REM Start a temporary Python server in the background
start /B python -m http.server 8888 >nul 2>&1

REM Wait a second for the server to start
timeout /t 2 /nobreak >nul

echo [2] Running admin setup...
REM Use curl or PowerShell to access the setup script
powershell -Command "Invoke-WebRequest -Uri 'http://localhost:8888/setup-admin.php' -OutFile setup_output.txt; Get-Content setup_output.txt"

echo.
echo ═══════════════════════════════════════════════════════════════
echo   Setup Complete!
echo ═══════════════════════════════════════════════════════════════
echo.

REM Kill the Python server
taskkill /F /IM python.exe >nul 2>&1

pause
