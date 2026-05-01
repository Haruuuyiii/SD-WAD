@echo off
REM ====================================================================
REM ADMIN DASHBOARD SYNC - QUICK START SCRIPT FOR WINDOWS
REM ====================================================================
REM This script starts all necessary services for admin dashboard sync
REM ====================================================================

echo.
echo ====================================================================
echo     ADMIN DASHBOARD - QUICK START
echo ====================================================================
echo.
echo Prerequisites:
echo   - XAMPP running with MySQL
echo   - Python 3.7+ installed
echo   - pip packages installed: flask, flask-cors, mysql-connector-python
echo.
echo Starting services...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

echo [1] Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2] Starting Admin Service (port 3003)...
echo Open new terminal and run:
echo   python admin_service.py
echo.

echo [3] Starting Auth Service (port 3001)...
echo Open new terminal and run:
echo   python auth_service.py
echo.

echo [4] Starting User Service (port 3002)...
echo Open new terminal and run:
echo   python user_service.py
echo.

echo ====================================================================
echo NEXT STEPS:
echo ====================================================================
echo.
echo 1. Make sure XAMPP MySQL is running (check phpMyAdmin works)
echo    → http://localhost/phpmyadmin
echo.
echo 2. In separate terminal windows, run each service:
echo    → python admin_service.py
echo    → python auth_service.py
echo    → python user_service.py
echo.
echo 3. Start Live Server for frontend:
echo    → Right-click main-page folder → Open with Live Server
echo.
echo 4. Open admin dashboard:
echo    → http://127.0.0.1:5500/WAD_SD/main-page/admin-dashboard.html
echo.
echo 5. Login with:
echo    Username: admin
echo    Password: 1234
echo.
echo 6. If you see "No data", insert test data in phpMyAdmin:
echo    → Check ADMIN_SYNC_SETUP.md for SQL queries
echo.
echo ====================================================================
echo.
pause
