#!/bin/bash

# ====================================================================
# ADMIN DASHBOARD SYNC - QUICK START SCRIPT FOR LINUX/MAC
# ====================================================================
# This script starts all necessary services for admin dashboard sync
# ====================================================================

echo ""
echo "===================================================================="
echo "     ADMIN DASHBOARD - QUICK START"
echo "===================================================================="
echo ""
echo "Prerequisites:"
echo "  - XAMPP running with MySQL"
echo "  - Python 3.7+ installed"
echo "  - pip packages installed: flask, flask-cors, mysql-connector-python"
echo ""
echo "Starting services..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Please install Python 3.7+"
    exit 1
fi

echo "[1] Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "[2] Starting Admin Service (port 3003)..."
echo "Open new terminal and run:"
echo "   python3 admin_service.py"
echo ""

echo "[3] Starting Auth Service (port 3001)..."
echo "Open new terminal and run:"
echo "   python3 auth_service.py"
echo ""

echo "[4] Starting User Service (port 3002)..."
echo "Open new terminal and run:"
echo "   python3 user_service.py"
echo ""

echo "===================================================================="
echo "NEXT STEPS:"
echo "===================================================================="
echo ""
echo "1. Make sure XAMPP MySQL is running (check phpMyAdmin works)"
echo "   → http://localhost/phpmyadmin"
echo ""
echo "2. In separate terminal windows, run each service:"
echo "   → python3 admin_service.py"
echo "   → python3 auth_service.py"
echo "   → python3 user_service.py"
echo ""
echo "3. Start Live Server for frontend:"
echo "   → Right-click main-page folder → Open with Live Server"
echo ""
echo "4. Open admin dashboard:"
echo "   → http://127.0.0.1:5500/WAD_SD/main-page/admin-dashboard.html"
echo ""
echo "5. Login with:"
echo "   Username: admin"
echo "   Password: 1234"
echo ""
echo "6. If you see 'No data', insert test data in phpMyAdmin:"
echo "   → Check ADMIN_SYNC_SETUP.md for SQL queries"
echo ""
echo "===================================================================="
echo ""
