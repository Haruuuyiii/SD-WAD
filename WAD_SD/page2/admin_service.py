# ─────────────────────────────────────────────────────────────
# ADMIN DASHBOARD SERVICE — admin_service.py
# Fetches real data from MySQL database for the admin dashboard
# Connects to XAMPP localhost MySQL database
#
# Run: python admin_service.py
# Runs on: http://localhost:3003
# ─────────────────────────────────────────────────────────────

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────────────────────
# DATABASE CONNECTION CONFIG
# ─────────────────────────────────────────────────────────────

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default XAMPP password is empty
    'database': 'sd-wad-main',
    'port': 3306
}

def get_db_connection():
    """Create a new database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

# ─────────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"service": "admin", "status": "ok", "database": "connected"})
    else:
        return jsonify({"service": "admin", "status": "error", "database": "disconnected"}), 500

# ─────────────────────────────────────────────────────────────
# DASHBOARD STATISTICS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    """Get all dashboard statistics"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    stats = {}
    
    try:
        # Total Events
        cursor.execute("SELECT COUNT(*) as count FROM events")
        stats['totalEvents'] = cursor.fetchone()['count'] or 0
        
        # Total Registrations
        cursor.execute("SELECT COUNT(*) as count FROM registrations")
        stats['totalRegistrations'] = cursor.fetchone()['count'] or 0
        
        # Active Events (events that haven't ended yet)
        cursor.execute("SELECT COUNT(*) as count FROM events WHERE event_end > NOW()")
        stats['activeEvents'] = cursor.fetchone()['count'] or 0
        
        # Tickets Bought/Checked In
        cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE checked_in = 1")
        stats['ticketsBought'] = cursor.fetchone()['count'] or 0
        
        # Logged In Users (you can customize this based on your sessions table)
        cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE last_login > DATE_SUB(NOW(), INTERVAL 1 HOUR)")
        stats['loggedInUsers'] = cursor.fetchone()['count'] or 0
        
        # Total Users (registered users)
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE role = 'user'")
        stats['totalUsers'] = cursor.fetchone()['count'] or 0
        
        return jsonify(stats)
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# EVENT REGISTRATIONS BY EVENT
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/registrations-by-event", methods=["GET"])
def get_registrations_by_event():
    """Get registration count per event"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT 
                e.event_id,
                e.event_name,
                COUNT(r.registration_id) as registrations,
                COALESCE(e.event_color, '#6366f1') as color
            FROM events e
            LEFT JOIN registrations r ON e.event_id = r.event_id
            GROUP BY e.event_id, e.event_name, e.event_color
            ORDER BY registrations DESC
            LIMIT 5
        """
        cursor.execute(query)
        events = cursor.fetchall()
        
        # Format response
        result = []
        colors = ['#3b82f6', '#f97316', '#06b6d4', '#8b5cf6', '#ec4899']
        for idx, event in enumerate(events):
            result.append({
                'name': event['event_name'],
                'registrations': event['registrations'],
                'color': event['color'] or colors[idx % len(colors)]
            })
        
        return jsonify({'eventRegistrations': result})
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# USER DISTRIBUTION (Registered, Attended, Pending)
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/user-distribution", methods=["GET"])
def get_user_distribution():
    """Get user distribution stats"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Registered (all registrations)
        cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE status = 'registered'")
        registered = cursor.fetchone()['count'] or 0
        
        # Attended (checked in)
        cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE checked_in = 1")
        attended = cursor.fetchone()['count'] or 0
        
        # Pending (not checked in yet)
        cursor.execute("SELECT COUNT(*) as count FROM registrations WHERE checked_in = 0 AND status = 'registered'")
        pending = cursor.fetchone()['count'] or 0
        
        return jsonify({
            'userDistribution': {
                'registered': registered,
                'attended': attended,
                'pending': pending
            }
        })
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# RECENT REGISTRATIONS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/recent-registrations", methods=["GET"])
def get_recent_registrations():
    """Get recent user registrations"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT 
                r.registration_id,
                u.first_name,
                u.last_name,
                u.email,
                e.event_name,
                r.created_at,
                r.checked_in,
                r.status
            FROM registrations r
            JOIN users u ON r.user_id = u.user_id
            JOIN events e ON r.event_id = e.event_id
            ORDER BY r.created_at DESC
            LIMIT 5
        """
        cursor.execute(query)
        registrations = cursor.fetchall()
        
        # Format response
        result = []
        for reg in registrations:
            # Calculate time ago
            created_time = reg['created_at']
            if isinstance(created_time, str):
                created_time = datetime.fromisoformat(created_time)
            time_diff = datetime.now() - created_time
            
            if time_diff.days > 0:
                time_ago = f"{time_diff.days} day{'s' if time_diff.days > 1 else ''} ago"
            elif time_diff.seconds > 3600:
                hours = time_diff.seconds // 3600
                time_ago = f"{hours} hour{'s' if hours > 1 else ''} ago"
            elif time_diff.seconds > 60:
                minutes = time_diff.seconds // 60
                time_ago = f"{minutes} minute{'s' if minutes > 1 else ''} ago"
            else:
                time_ago = "Just now"
            
            # Determine badge status
            if reg['checked_in']:
                badge = 'verified'
                badge_text = 'Verified'
            elif reg['status'] == 'pending':
                badge = 'pending'
                badge_text = 'Pending'
            else:
                badge = 'verified'
                badge_text = 'Verified'
            
            result.append({
                'name': f"{reg['first_name']} {reg['last_name']}",
                'initials': (reg['first_name'][0] + reg['last_name'][0]).upper(),
                'event': reg['event_name'],
                'time': time_ago,
                'badge': badge,
                'badge_text': badge_text
            })
        
        return jsonify({'recentRegistrations': result})
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# ALL EVENTS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/events", methods=["GET"])
def get_all_events():
    """Get all events"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT 
                e.event_id,
                e.event_name,
                e.event_description,
                e.event_start,
                e.event_end,
                e.location,
                COUNT(r.registration_id) as total_registrations
            FROM events e
            LEFT JOIN registrations r ON e.event_id = r.event_id
            GROUP BY e.event_id
            ORDER BY e.event_start DESC
        """
        cursor.execute(query)
        events = cursor.fetchall()
        
        return jsonify({'events': events})
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# ALL REGISTRATIONS
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/registrations", methods=["GET"])
def get_all_registrations():
    """Get all registrations"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT 
                r.registration_id,
                u.user_id,
                u.first_name,
                u.last_name,
                u.email,
                e.event_name,
                r.created_at,
                r.checked_in,
                r.status
            FROM registrations r
            JOIN users u ON r.user_id = u.user_id
            JOIN events e ON r.event_id = e.event_id
            ORDER BY r.created_at DESC
        """
        cursor.execute(query)
        registrations = cursor.fetchall()
        
        return jsonify({'registrations': registrations})
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# ATTENDANCE DATA
# ─────────────────────────────────────────────────────────────

@app.route("/dashboard/attendance", methods=["GET"])
def get_attendance():
    """Get attendance statistics by event"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT 
                e.event_name,
                COUNT(r.registration_id) as total_registered,
                SUM(CASE WHEN r.checked_in = 1 THEN 1 ELSE 0 END) as attended,
                ROUND(100.0 * SUM(CASE WHEN r.checked_in = 1 THEN 1 ELSE 0 END) / COUNT(r.registration_id), 2) as attendance_rate
            FROM events e
            LEFT JOIN registrations r ON e.event_id = r.event_id
            GROUP BY e.event_id, e.event_name
            ORDER BY e.event_start DESC
        """
        cursor.execute(query)
        attendance = cursor.fetchall()
        
        return jsonify({'attendance': attendance})
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# ERROR HANDLER
# ─────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    print("=" * 60)
    print("  ADMIN DASHBOARD SERVICE")
    print("=" * 60)
    print("  Database: localhost/sd-wad-main")
    print("  Running on: http://localhost:3003")
    print("  CORS: Enabled for frontend")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET  /health")
    print("  GET  /dashboard/stats")
    print("  GET  /dashboard/registrations-by-event")
    print("  GET  /dashboard/user-distribution")
    print("  GET  /dashboard/recent-registrations")
    print("  GET  /dashboard/events")
    print("  GET  /dashboard/registrations")
    print("  GET  /dashboard/attendance")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=3003, host='0.0.0.0')
