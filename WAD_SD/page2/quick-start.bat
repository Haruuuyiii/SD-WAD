@echo off
REM ═══════════════════════════════════════════════════════════════
REM CozMoz Event Management System - Quick Start
REM Windows Batch Script
REM ═══════════════════════════════════════════════════════════════

echo.
echo ═══════════════════════════════════════════════════════════════
echo  CozMoz Event Management System - Quick Start Setup
echo ═══════════════════════════════════════════════════════════════
echo.

REM Step 1: Check if XAMPP MySQL is running
echo Step 1: Checking XAMPP MySQL...
netstat -ano | find "3306" >nul
if errorlevel 1 (
    echo   [ERROR] MySQL is not running!
    echo   Please start XAMPP and ensure MySQL is running (green status)
    echo   Then run this script again.
    pause
    exit /b 1
) else (
    echo   [OK] MySQL is running on port 3306
)

echo.
echo Step 2: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Python is not installed or not in PATH!
    echo   Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do echo   [OK] Python %%i is installed
)

echo.
echo Step 3: Installing/Updating Python dependencies...
echo   Installing: Flask, Flask-CORS, mysql-connector-python...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo   [ERROR] Failed to install dependencies!
    echo   Please ensure pip is installed and working
    pause
    exit /b 1
) else (
    echo   [OK] Dependencies installed successfully
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo  Setup Complete!
echo ═══════════════════════════════════════════════════════════════
echo.
echo Next steps:
echo.
echo 1. Initialize the database:
echo    - Open: http://localhost/phpmyadmin
echo    - Import: page2/database-init.sql
echo.
echo 2. Start the Admin Service:
echo    - This script can automatically start it
echo    - Press Enter to continue or type 'n' to skip...
echo.
set /p startservice="Start admin_service.py now? (y/n): "
if /i "%startservice%"=="y" (
    echo.
    echo Starting admin_service.py on port 3003...
    echo Press Ctrl+C to stop the service
    echo.
    python admin_service.py
) else (
    echo.
    echo To start admin_service.py manually, run:
    echo   python admin_service.py
    echo.
    echo Then access the admin dashboard at:
    echo   http://localhost/path/to/admin-login.html
    echo.
    echo Admin credentials:
    echo   Username: admin
    echo   Password: admin123
    echo.
    pause
)
