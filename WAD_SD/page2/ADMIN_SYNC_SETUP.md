# Admin Dashboard Database Synchronization Guide

## Overview
The admin dashboard is now synchronized with your MySQL database through a Python Flask backend service. Real-time data from your XAMPP localhost database will display on the admin dashboard.

## Architecture
```
XAMPP MySQL Database (sd-wad-main)
         ↑
         └─── admin_service.py (Flask API on port 3003)
                     ↑
                     └─── admin-dashboard.html (Frontend)
                                + admin-dashboard-script.js
```

## Prerequisites
- Python 3.7+ installed
- XAMPP running with MySQL service active
- Database: `sd-wad-main` with required tables
- Node.js + npm (or just use Live Server for frontend)

## Step 1: Install Python Dependencies

Run this command in the `page2` folder:

```bash
pip install flask flask-cors mysql-connector-python
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

## Step 2: Verify Database Connection

Make sure your XAMPP MySQL is running with:
- **Host:** localhost
- **Port:** 3306
- **Username:** root
- **Password:** (empty by default)
- **Database:** sd-wad-main

Test connection by opening phpMyAdmin:
```
http://localhost/phpmyadmin
```

## Step 3: Create Database Tables (if not exists)

Run these SQL queries in phpMyAdmin to create the required tables:

```sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
  user_id INT PRIMARY KEY AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  role VARCHAR(20) DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE IF NOT EXISTS events (
  event_id INT PRIMARY KEY AUTO_INCREMENT,
  event_name VARCHAR(100) NOT NULL,
  event_description TEXT,
  event_start DATETIME,
  event_end DATETIME,
  location VARCHAR(100),
  event_color VARCHAR(7),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Registrations table
CREATE TABLE IF NOT EXISTS registrations (
  registration_id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  event_id INT NOT NULL,
  status VARCHAR(20) DEFAULT 'registered',
  checked_in BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (event_id) REFERENCES events(event_id)
);

-- Add optional: last_login column to users
ALTER TABLE users ADD COLUMN last_login DATETIME;
```

## Step 4: Start the Admin Service

Navigate to the `page2` folder and run:

```bash
python admin_service.py
```

You should see:
```
============================================================
  ADMIN DASHBOARD SERVICE
============================================================
  Database: localhost/sd-wad-main
  Running on: http://localhost:3003
  CORS: Enabled for frontend
============================================================

Endpoints:
  GET  /health
  GET  /dashboard/stats
  GET  /dashboard/registrations-by-event
  GET  /dashboard/user-distribution
  GET  /dashboard/recent-registrations
  GET  /dashboard/events
  GET  /dashboard/registrations
  GET  /dashboard/attendance
============================================================
```

## Step 5: Load Admin Dashboard

1. Open admin dashboard in browser:
   ```
   http://127.0.0.1:5500/WAD_SD/main-page/admin-dashboard.html
   ```

2. Log in if prompted (credentials set in auth_service.py)
   - Username: `admin`
   - Password: `1234`

3. Dashboard will auto-fetch data from the database every 30 seconds

## Available API Endpoints

### Get Dashboard Statistics
```
GET /dashboard/stats
```
Returns: `totalEvents`, `totalRegistrations`, `activeEvents`, `ticketsBought`, `loggedInUsers`, `totalUsers`

### Get Registrations by Event
```
GET /dashboard/registrations-by-event
```
Returns bar chart data with event names and registration counts

### Get User Distribution
```
GET /dashboard/user-distribution
```
Returns: `registered`, `attended`, `pending` counts

### Get Recent Registrations
```
GET /dashboard/recent-registrations
```
Returns last 5 user registrations with names, events, and timestamps

### Get All Events
```
GET /dashboard/events
```
Returns complete list of all events with details

### Get All Registrations
```
GET /dashboard/registrations
```
Returns complete list of all registrations

### Get Attendance Data
```
GET /dashboard/attendance
```
Returns attendance statistics by event with attendance rates

## Troubleshooting

### Issue: "Failed to Connect to Database"
**Solution:**
- Check XAMPP MySQL is running
- Verify database name is `sd-wad-main`
- Check credentials in `admin_service.py` DB_CONFIG

### Issue: "Admin service not responding"
**Solution:**
- Make sure `admin_service.py` is running on port 3003
- Check no firewall is blocking port 3003
- Run: `python admin_service.py`

### Issue: Dashboard shows "No data"
**Solution:**
- Add test data to your database first
- Check browser console for error messages (F12)
- Verify API endpoints are working: `http://localhost:3003/health`

### Issue: CORS Error
**Solution:**
- Flask CORS is already enabled in `admin_service.py`
- Make sure you're accessing from `http://127.0.0.1:5500`, not `localhost`

## Testing Data

Insert sample test data:

```sql
-- Insert test users
INSERT INTO users (first_name, last_name, email, role) VALUES
('Admin', 'User', 'admin@cozmoz.com', 'admin'),
('John', 'Doe', 'john@example.com', 'user'),
('Jane', 'Smith', 'jane@example.com', 'user');

-- Insert test events
INSERT INTO events (event_name, event_description, event_start, event_end, location, event_color) VALUES
('TechTalk 2024', 'Amazing tech conference', '2024-06-01 09:00:00', '2024-06-01 17:00:00', 'Manila', '#3b82f6'),
('Web Dev Workshop', 'Learn modern web development', '2024-06-15 10:00:00', '2024-06-15 16:00:00', 'Quezon City', '#f97316');

-- Insert test registrations
INSERT INTO registrations (user_id, event_id, status, checked_in) VALUES
(2, 1, 'registered', 1),
(3, 1, 'registered', 0),
(2, 2, 'registered', 0);
```

Then refresh the admin dashboard to see the data appear!

## Auto-Refresh

The dashboard automatically:
- Fetches data on page load
- Updates charts when period selector changes
- Auto-refreshes all data every 30 seconds

To change refresh interval, edit `admin-dashboard-script.js`:
```javascript
// Change from 30000 to your desired milliseconds
setInterval(() => {
  loadDashboardData();
}, 30000);  // 30 seconds
```

## Services Running

You should have these services running:
1. **XAMPP MySQL** - Database server (port 3306)
2. **admin_service.py** - Admin API (port 3003)
3. **auth_service.py** - Authentication (port 3001)
4. **user_service.py** - User profiles (port 3002)
5. **Live Server** - Frontend (port 5500)

## Command Reference

Start all services:
```bash
# Terminal 1: Admin Service
python page2/admin_service.py

# Terminal 2: Auth Service
python page2/auth_service.py

# Terminal 3: User Service
python page2/user_service.py

# Terminal 4: Start XAMPP MySQL
# Open XAMPP Control Panel and click Start for MySQL

# Terminal 5: Start Live Server
# VS Code: Right-click main-page folder → Open with Live Server
```

## Next Steps

1. ✅ Set up the admin service
2. ✅ Connect to database
3. ✅ Add test data
4. 📊 View real-time dashboard
5. 🔧 Customize tables as needed
6. 🚀 Deploy to production

## Support

For issues or questions:
- Check `app.log` in `page2/` folder for error logs
- Verify all prerequisites are installed
- Test each API endpoint manually using a REST client (Postman, etc.)

---

**Created:** May 1, 2026
**Version:** 1.0
**Status:** Ready for production use
