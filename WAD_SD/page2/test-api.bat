@echo off
REM ═══════════════════════════════════════════════════════════════
REM CozMoz - Complete Testing Guide
REM Test all API endpoints and features
REM ═══════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ═══════════════════════════════════════════════════════════════
echo  CozMoz Event Management System - API Testing Guide
echo ═══════════════════════════════════════════════════════════════
echo.

echo Prerequisites:
echo   - XAMPP MySQL running on port 3306
echo   - admin_service.py running on port 3003
echo   - Database initialized with database-init.sql
echo.

:MENU
cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  TEST OPTIONS
echo ═══════════════════════════════════════════════════════════════
echo.
echo 1. Test Health/Connection
echo 2. Test Admin Login
echo 3. Register New User
echo 4. User Login
echo 5. Buy Ticket
echo 6. Check In
echo 7. Get Dashboard Stats
echo 8. Get All Events
echo.
echo 0. Exit
echo.
set /p choice="Select an option (0-8): "

if "%choice%"=="1" goto TEST_HEALTH
if "%choice%"=="2" goto TEST_ADMIN_LOGIN
if "%choice%"=="3" goto TEST_REGISTER
if "%choice%"=="4" goto TEST_USER_LOGIN
if "%choice%"=="5" goto TEST_BUY_TICKET
if "%choice%"=="6" goto TEST_CHECK_IN
if "%choice%"=="7" goto TEST_STATS
if "%choice%"=="8" goto TEST_EVENTS
if "%choice%"=="0" goto END
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 1: Health Check
REM ═══════════════════════════════════════════════════════════════
:TEST_HEALTH
cls
echo.
echo Testing Health Endpoint...
echo Command: curl http://localhost:3003/health
echo.
curl -s http://localhost:3003/health | findstr /r "service" >nul
if errorlevel 1 (
    echo [ERROR] Service not responding!
    echo Make sure admin_service.py is running on port 3003
) else (
    echo [OK] Service is running
    curl -s http://localhost:3003/health
)
echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 2: Admin Login
REM ═══════════════════════════════════════════════════════════════
:TEST_ADMIN_LOGIN
cls
echo.
echo Testing Admin Login...
echo Command: curl -X POST http://localhost:3003/admin/login
echo Credentials: username=admin, password=admin123
echo.

setlocal enabledelayedexpansion
for /f "tokens=*" %%A in ('
  curl -s -X POST http://localhost:3003/admin/login ^
    -H "Content-Type: application/json" ^
    -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
') do (
  set "response=%%A"
)

echo Response: !response!

if "!response!" find "token" >nul (
    echo [OK] Login successful!
    for /f "tokens=2 delims=:," %%A in ('echo !response! ^| findstr /r "token"') do (
        set "token=%%A"
        set "token=!token:"=!"
        set "token=!token: =!"
    )
    echo Admin token: !token!
) else (
    echo [ERROR] Login failed. Make sure admin user exists in database.
)

endlocal
echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 3: Register New User
REM ═══════════════════════════════════════════════════════════════
:TEST_REGISTER
cls
echo.
echo Testing User Registration...
echo.

set /p username="Enter username: "
set /p email="Enter email: "
set /p password="Enter password: "
set /p first_name="Enter first name: "
set /p last_name="Enter last name: "

echo.
echo Registering user...

for /f "tokens=*" %%A in ('
  curl -s -X POST http://localhost:3003/register ^
    -H "Content-Type: application/json" ^
    -d "{\"username\":\"!username!\",\"email\":\"!email!\",\"password\":\"!password!\",\"first_name\":\"!first_name!\",\"last_name\":\"!last_name!\"}"
') do (
  set "response=%%A"
)

echo Response: !response!

if "!response!" find "user_id" >nul (
    echo [OK] Registration successful!
    for /f "tokens=2 delims=:" %%A in ('echo !response! ^| findstr "user_id"') do (
        set "user_id=%%A"
        set "user_id=!user_id:,=!"
    )
    echo User ID: !user_id!
) else (
    echo [ERROR] Registration failed
)

echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 4: User Login
REM ═══════════════════════════════════════════════════════════════
:TEST_USER_LOGIN
cls
echo.
echo Testing User Login...
echo.

set /p username="Enter username: "
set /p password="Enter password: "

echo.
echo Logging in...

for /f "tokens=*" %%A in ('
  curl -s -X POST http://localhost:3003/login ^
    -H "Content-Type: application/json" ^
    -d "{\"username\":\"!username!\",\"password\":\"!password!\"}"
') do (
  set "response=%%A"
)

echo Response: !response!

if "!response!" find "user_id" >nul (
    echo [OK] Login successful!
) else (
    echo [ERROR] Login failed
)

echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 5: Buy Ticket
REM ═══════════════════════════════════════════════════════════════
:TEST_BUY_TICKET
cls
echo.
echo Testing Ticket Purchase...
echo.
echo Note: First check available events using option 8
echo.

set /p user_id="Enter user ID: "
set /p event_id="Enter event ID: "

echo.
echo Purchasing ticket...

for /f "tokens=*" %%A in ('
  curl -s -X POST http://localhost:3003/buy-ticket ^
    -H "Content-Type: application/json" ^
    -d "{\"user_id\":!user_id!,\"event_id\":!event_id!}"
') do (
  set "response=%%A"
)

echo Response: !response!

if "!response!" find "ticket_code" >nul (
    echo [OK] Ticket purchased successfully!
    for /f "tokens=2 delims=:," %%A in ('echo !response! ^| findstr "ticket_code"') do (
        set "ticket_code=%%A"
        set "ticket_code=!ticket_code:"=!"
    )
    echo Ticket Code: !ticket_code!
    echo Save this code for check-in test
) else (
    echo [ERROR] Ticket purchase failed
)

echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 6: Check In
REM ═══════════════════════════════════════════════════════════════
:TEST_CHECK_IN
cls
echo.
echo Testing Check In...
echo.

set /p ticket_code="Enter ticket code to check in: "

echo.
echo Processing check in...

for /f "tokens=*" %%A in ('
  curl -s -X POST http://localhost:3003/check-in ^
    -H "Content-Type: application/json" ^
    -d "{\"ticket_code\":\"!ticket_code!\"}"
') do (
  set "response=%%A"
)

echo Response: !response!

if "!response!" find "Successfully" >nul (
    echo [OK] Check in successful!
) else (
    echo [ERROR] Check in failed
)

echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 7: Dashboard Stats
REM ═══════════════════════════════════════════════════════════════
:TEST_STATS
cls
echo.
echo Getting Dashboard Statistics...
echo.

for /f "tokens=*" %%A in ('
  curl -s http://localhost:3003/dashboard/stats
') do (
  set "response=%%A"
)

echo Response:
echo !response!

echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
REM TEST 8: Get All Events
REM ═══════════════════════════════════════════════════════════════
:TEST_EVENTS
cls
echo.
echo Getting Available Events...
echo.

for /f "tokens=*" %%A in ('
  curl -s http://localhost:3003/events
') do (
  set "response=%%A"
)

echo Response:
echo !response!

echo.
pause
goto MENU

REM ═══════════════════════════════════════════════════════════════
:END
echo.
echo Goodbye!
echo.
