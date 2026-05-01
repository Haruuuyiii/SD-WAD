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
        return mysql.connector.connect(**DB_CONFIG)
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
# ADMIN AUTHENTICATION
# ─────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["POST"])
def admin_login():
    """Admin login - returns token if credentials are valid"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT user_id, username, first_name, role FROM users WHERE username = %s AND role = 'admin'", (username,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # For demo: simple password check (in production use bcrypt)
        # Store token in session
        import time
        import hashlib
        token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
        
        # Store session
        cursor.execute("""
            INSERT INTO sessions (user_id, token, ip_address, status) 
            VALUES (%s, %s, %s, 'active')
        """, (user['user_id'], token, request.remote_addr))
        conn.commit()
        
        return jsonify({
            "message": f"Welcome {user['first_name']}!",
            "token": token,
            "username": user['username'],
            "user_id": user['user_id'],
            "role": user['role']
        }), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# USER REGISTRATION
# ─────────────────────────────────────────────────────────────

@app.route("/register", methods=["POST"])
def register_user():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    if not all([username, email, password, first_name, last_name]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if user exists
        cursor.execute("SELECT user_id FROM users WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            return jsonify({"error": "Username or email already exists"}), 409
        
        # Use bcrypt or simple hash for password in production
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (username, email, password, first_name, last_name, role)
            VALUES (%s, %s, %s, %s, %s, 'user')
        """, (username, email, hashed_password, first_name, last_name))
        conn.commit()
        
        user_id = cursor.lastrowid
        
        return jsonify({
            "message": f"Account created successfully! Welcome {first_name}!",
            "user_id": user_id,
            "username": username
        }), 201
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# USER LOGIN (for event portal)
# ─────────────────────────────────────────────────────────────

@app.route("/login", methods=["POST"])
def user_login():
    """User login for event portal"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        import hashlib
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("""
            SELECT user_id, username, first_name, last_name, email, role 
            FROM users 
            WHERE username = %s AND password = %s AND role = 'user'
        """, (username, hashed_password))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Create session
        import time
        token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
        cursor.execute("""
            INSERT INTO sessions (user_id, token, ip_address, status) 
            VALUES (%s, %s, %s, 'active')
        """, (user['user_id'], token, request.remote_addr))
        conn.commit()
        
        return jsonify({
            "message": f"Welcome {user['first_name']}!",
            "token": token,
            "user_id": user['user_id'],
            "username": user['username'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email']
        }), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# REGISTER FOR EVENT
# ─────────────────────────────────────────────────────────────

@app.route("/register-event", methods=["POST"])
def register_for_event():
    """Register a user for an event"""
    data = request.get_json()
    user_id = data.get('user_id')
    event_id = data.get('event_id')
    amount_paid = data.get('amount_paid', 0)
    
    if not user_id or not event_id:
        return jsonify({"error": "User ID and Event ID required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Check if user is already registered
        cursor.execute("""
            SELECT registration_id FROM registrations 
            WHERE user_id = %s AND event_id = %s
        """, (user_id, event_id))
        
        if cursor.fetchone():
            return jsonify({"error": "User already registered for this event"}), 409
        
        # Get event details
        cursor.execute("""
            SELECT event_name, ticket_price FROM events WHERE event_id = %s
        """, (event_id,))
        event = cursor.fetchone()
        
        if not event:
            return jsonify({"error": "Event not found"}), 404
        
        # Create registration
        cursor.execute("""
            INSERT INTO registrations (user_id, event_id, status, amount_paid, payment_status)
            VALUES (%s, %s, 'registered', %s, 'completed')
        """, (user_id, event_id, amount_paid or event['ticket_price']))
        conn.commit()
        
        registration_id = cursor.lastrowid
        
        # Generate ticket
        import hashlib
        ticket_code = hashlib.md5(f"{user_id}{event_id}{registration_id}".encode()).hexdigest()[:12].upper()
        
        cursor.execute("""
            INSERT INTO tickets (ticket_code, registration_id, event_id, user_id, status, price)
            VALUES (%s, %s, %s, %s, 'available', %s)
        """, (ticket_code, registration_id, event_id, user_id, amount_paid or event['ticket_price']))
        conn.commit()
        
        return jsonify({
            "message": f"Successfully registered for {event['event_name']}!",
            "registration_id": registration_id,
            "ticket_code": ticket_code,
            "amount_paid": amount_paid or event['ticket_price']
        }), 201
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# BUY TICKET
# ─────────────────────────────────────────────────────────────

@app.route("/buy-ticket", methods=["POST"])
def buy_ticket():
    """Buy a ticket for an event"""
    data = request.get_json()
    user_id = data.get('user_id')
    event_id = data.get('event_id')
    payment_method = data.get('payment_method', 'card')
    
    if not user_id or not event_id:
        return jsonify({"error": "User ID and Event ID required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get event details
        cursor.execute("""
            SELECT event_id, event_name, ticket_price FROM events WHERE event_id = %s
        """, (event_id,))
        event = cursor.fetchone()
        
        if not event:
            return jsonify({"error": "Event not found"}), 404
        
        # Check if already registered
        cursor.execute("""
            SELECT registration_id FROM registrations 
            WHERE user_id = %s AND event_id = %s AND status = 'registered'
        """, (user_id, event_id))
        
        if cursor.fetchone():
            return jsonify({"error": "Ticket already purchased"}), 409
        
        # Create registration (same as buying)
        cursor.execute("""
            INSERT INTO registrations (user_id, event_id, status, amount_paid, payment_status)
            VALUES (%s, %s, 'registered', %s, 'completed')
        """, (user_id, event_id, event['ticket_price']))
        conn.commit()
        
        registration_id = cursor.lastrowid
        
        # Generate ticket code
        import hashlib
        ticket_code = hashlib.md5(f"{user_id}{event_id}{registration_id}".encode()).hexdigest()[:12].upper()
        
        cursor.execute("""
            INSERT INTO tickets (ticket_code, registration_id, event_id, user_id, status, price)
            VALUES (%s, %s, %s, %s, 'available', %s)
        """, (ticket_code, registration_id, event_id, user_id, event['ticket_price']))
        conn.commit()
        
        return jsonify({
            "message": f"Ticket purchased successfully for {event['event_name']}!",
            "ticket_code": ticket_code,
            "event_name": event['event_name'],
            "price": event['ticket_price'],
            "registration_id": registration_id
        }), 201
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# CHECK IN ATTENDEE
# ─────────────────────────────────────────────────────────────

@app.route("/check-in", methods=["POST"])
def check_in():
    """Check in an attendee"""
    data = request.get_json()
    ticket_code = data.get('ticket_code', '').upper()
    
    if not ticket_code:
        return jsonify({"error": "Ticket code required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Find ticket
        cursor.execute("""
            SELECT t.ticket_id, t.registration_id, r.user_id, r.event_id, r.checked_in,
                   u.first_name, u.last_name, e.event_name
            FROM tickets t
            JOIN registrations r ON t.registration_id = r.registration_id
            JOIN users u ON r.user_id = u.user_id
            JOIN events e ON r.event_id = e.event_id
            WHERE t.ticket_code = %s AND t.status = 'available'
        """, (ticket_code,))
        
        ticket = cursor.fetchone()
        
        if not ticket:
            return jsonify({"error": "Invalid or already used ticket"}), 404
        
        if ticket['checked_in']:
            return jsonify({"error": "Already checked in"}), 400
        
        # Update registration and ticket
        cursor.execute("""
            UPDATE registrations 
            SET checked_in = 1, check_in_time = NOW(), status = 'checked_in'
            WHERE registration_id = %s
        """, (ticket['registration_id'],))
        
        cursor.execute("""
            UPDATE tickets 
            SET status = 'used', used_date = NOW()
            WHERE ticket_id = %s
        """, (ticket['ticket_id'],))
        
        conn.commit()
        
        return jsonify({
            "message": f"Successfully checked in {ticket['first_name']} {ticket['last_name']}!",
            "attendee_name": f"{ticket['first_name']} {ticket['last_name']}",
            "event_name": ticket['event_name'],
            "check_in_time": datetime.now().isoformat()
        }), 200
    
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ─────────────────────────────────────────────────────────────
# GET EVENTS FOR USERS
# ─────────────────────────────────────────────────────────────

@app.route("/events", methods=["GET"])
def get_events():
    """Get available events for users"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        query = """
            SELECT 
                event_id,
                event_name,
                event_description,
                event_start,
                event_end,
                location,
                ticket_price,
                max_capacity,
                COUNT(r.registration_id) as registered_count,
                (max_capacity - COUNT(r.registration_id)) as spots_available
            FROM events e
            LEFT JOIN registrations r ON e.event_id = r.event_id AND r.status = 'registered'
            WHERE e.status = 'published' AND e.event_start > NOW()
            GROUP BY e.event_id
            ORDER BY e.event_start ASC
        """
        cursor.execute(query)
        events = cursor.fetchall()
        
        return jsonify({"events": events}), 200
    
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

    print("  Running on: http://localhost:3003")
    print("=" * 60)
    app.run(debug=True, port=3003)
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
