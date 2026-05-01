# ─────────────────────────────────────────────────────────────
# ADMIN DASHBOARD SERVICE — admin_service.py
# Fetches data via PHP API endpoints instead of direct MySQL
# Connects to PHP-based database through HTTP API
#
# Run: python admin_service.py
# Runs on: http://localhost:3003
# ─────────────────────────────────────────────────────────────

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────────────────────
# PHP API BASE URL CONFIGURATION
# ─────────────────────────────────────────────────────────────

PHP_API_BASE_URL = "http://localhost/SD-WAD/WAD_SD/page2/api.php"

def call_php_api(endpoint, method='GET', data=None):
    """
    Call PHP API endpoint
    
    Args:
        endpoint: API endpoint path (e.g., 'dashboard/stats')
        method: HTTP method (GET, POST)
        data: JSON data for POST requests
    
    Returns:
        Response data or None if failed
    """
    try:
        url = f"{PHP_API_BASE_URL}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            return None
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling PHP API: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    result = call_php_api("health")
    if result:
        return jsonify({"service": "admin", "status": "ok", "database": "connected"})
    else:
        return jsonify({"service": "admin", "status": "error", "database": "disconnected"}), 500

# ─────────────────────────────────────────────────────────────
# DASHBOARD STATISTICS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    """Get all dashboard statistics via PHP API"""
    result = call_php_api("dashboard/stats")
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch stats from API"}), 500

# ─────────────────────────────────────────────────────────────
# EVENT REGISTRATIONS BY EVENT
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/registrations-by-event", methods=["GET"])
def get_registrations_by_event():
    """Get registration count per event via PHP API"""
    result = call_php_api("dashboard/registrations-by-event")
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500

# ─────────────────────────────────────────────────────────────
# USER DISTRIBUTION (Registered, Attended, Pending)
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/user-distribution", methods=["GET"])
def get_user_distribution():
    """Get user distribution stats via PHP API"""
    result = call_php_api("dashboard/user-distribution")
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500

# ─────────────────────────────────────────────────────────────
# RECENT REGISTRATIONS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/recent-registrations", methods=["GET"])
def get_recent_registrations():
    """Get recent user registrations via PHP API"""
    result = call_php_api("dashboard/recent-registrations")
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500

# ─────────────────────────────────────────────────────────────
# ALL EVENTS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/events", methods=["GET"])
def get_all_events():
    """Get all events via PHP API"""
    result = call_php_api("dashboard/events")
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500

# ─────────────────────────────────────────────────────────────
# ALL REGISTRATIONS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/registrations", methods=["GET"])
def get_all_registrations():
    """Get all registrations via PHP API"""
    result = call_php_api("dashboard/registrations")
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500

# ─────────────────────────────────────────────────────────────
# ATTENDANCE DATA
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/attendance", methods=["GET"])
def get_attendance():
    """Get attendance statistics by event via PHP API"""
    result = call_php_api("dashboard/attendance")
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed to fetch data from API"}), 500

# ─────────────────────────────────────────────────────────────
# ADMIN AUTHENTICATION
# ─────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["POST"])
def admin_login():
    """Admin login via PHP API"""
    data = request.get_json()
    result = call_php_api("admin/login", method='POST', data=data)
    if result:
        return jsonify(result), 200 if 'token' in result else 401
    else:
        return jsonify({"error": "Login failed"}), 500

# ─────────────────────────────────────────────────────────────
# USER REGISTRATION
# ─────────────────────────────────────────────────────────────

@app.route("/register", methods=["POST"])
def register_user():
    """Register a new user via PHP API"""
    data = request.get_json()
    result = call_php_api("register", method='POST', data=data)
    if result:
        return jsonify(result), 201 if 'user_id' in result else 409
    else:
        return jsonify({"error": "Registration failed"}), 500

# ─────────────────────────────────────────────────────────────
# USER LOGIN (for event portal)
# ─────────────────────────────────────────────────────────────

@app.route("/login", methods=["POST"])
def user_login():
    """User login for event portal via PHP API"""
    data = request.get_json()
    result = call_php_api("login", method='POST', data=data)
    if result:
        return jsonify(result), 200 if 'token' in result else 401
    else:
        return jsonify({"error": "Login failed"}), 500

# ─────────────────────────────────────────────────────────────
# REGISTER FOR EVENT
# ─────────────────────────────────────────────────────────────

@app.route("/register-event", methods=["POST"])
def register_for_event():
    """Register a user for an event via PHP API"""
    data = request.get_json()
    result = call_php_api("register-event", method='POST', data=data)
    if result:
        return jsonify(result), 201 if 'registration_id' in result else 409
    else:
        return jsonify({"error": "Event registration failed"}), 500

# ─────────────────────────────────────────────────────────────
# BUY TICKET
# ─────────────────────────────────────────────────────────────

@app.route("/buy-ticket", methods=["POST"])
def buy_ticket():
    """Buy a ticket for an event via PHP API"""
    data = request.get_json()
    result = call_php_api("buy-ticket", method='POST', data=data)
    if result:
        return jsonify(result), 201 if 'ticket_code' in result else 409
    else:
        return jsonify({"error": "Ticket purchase failed"}), 500

# ─────────────────────────────────────────────────────────────
# CHECK IN ATTENDEE
# ─────────────────────────────────────────────────────────────

@app.route("/check-in", methods=["POST"])
def check_in():
    """Check in an attendee via PHP API"""
    data = request.get_json()
    result = call_php_api("check-in", method='POST', data=data)
    if result:
        return jsonify(result), 200 if 'attendee_name' in result else 404
    else:
        return jsonify({"error": "Check-in failed"}), 500

# ─────────────────────────────────────────────────────────────
# GET EVENTS FOR USERS
# ─────────────────────────────────────────────────────────────

@app.route("/events", methods=["GET"])
def get_events():
    """Get available events for users via PHP API"""
    result = call_php_api("events")
    if result:
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to fetch events"}), 500

# ─────────────────────────────────────────────────────────────
# ERROR HANDLER
# ─────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500
