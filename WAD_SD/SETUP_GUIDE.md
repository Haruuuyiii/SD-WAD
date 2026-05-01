# CozMoz Event Management System - Complete Setup Guide

## 📋 Table of Contents
1. [Database Setup](#database-setup)
2. [Running Services](#running-services)
3. [Admin Dashboard](#admin-dashboard)
4. [User Registration & Tickets](#user-registration--tickets)
5. [Troubleshooting](#troubleshooting)

---

## 🗄️ Database Setup

### 1. Initialize the Database

First, open **phpMyAdmin** in your browser:
- URL: `http://localhost/phpmyadmin`
- Username: `root`
- Password: (leave empty - default XAMPP)

### 2. Create Database and Tables

**Option A: Using phpMyAdmin (Recommended)**

1. Click "SQL" tab
2. Copy the entire contents of `page2/database-init.sql`
3. Paste into the SQL editor
4. Click "Go" to execute

**Option B: Using Command Line**

```bash
# Navigate to page2 folder
cd C:\Users\Adrein\Documents\GitHub\SD-WAD\WAD_SD\page2

# Run the SQL file
mysql -u root -D sd-wad-main < database-init.sql
```

### 3. Verify Database Setup

Check that these tables were created:
- `users` - Stores user accounts
- `events` - Stores event information
- `registrations` - Stores event registrations
- `tickets` - Stores individual tickets
- `sessions` - Stores login sessions

---

## 🚀 Running Services

### Step 1: Start XAMPP MySQL
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL
3. Wait until it shows "running" in green

### Step 2: Start Admin Service

Open PowerShell/Command Prompt in the `page2` folder:

```bash
cd C:\Users\Adrein\Documents\GitHub\SD-WAD\WAD_SD\page2
python admin_service.py
```

Expected output:
```
============================================================
  ADMIN DASHBOARD SERVICE
============================================================
  Database: localhost/sd-wad-main
  Running on: http://localhost:3003
============================================================
 * Running on http://127.0.0.1:3003
 * Debug mode: on
```

### Step 3: Verify Services are Running

Test the health endpoints:

```bash
# Test admin service
curl http://localhost:3003/health

# Expected response:
# {"service": "admin", "status": "ok", "database": "connected"}
```

---

## 🔐 Admin Dashboard

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

### Accessing Admin Dashboard

1. Open browser and navigate to: `http://localhost/path/to/admin-login.html`
2. Enter admin credentials
3. Click "Sign In"

### Admin Dashboard Features

| Feature | Description |
|---------|-------------|
| **Dashboard** | View summary statistics (0 when database is empty) |
| **Events** | Create and manage events |
| **Registrations** | View all user registrations |
| **Attendance** | Track event check-ins |
| **Analytics** | View detailed statistics and charts |
| **Announcements** | Send notifications to users |

### Dashboard Stats Explained

When database is empty, these will show **0**:
- **Total Events**: Number of created events
- **Total Registrations**: Number of ticket purchases
- **Active Events**: Events currently happening
- **Tickets Bought**: Number of checked-in attendees
- **Logged In Users**: Users logged in within the last hour
- **Total Users**: Total registered user accounts

---

## 👥 User Registration & Tickets

### User Registration Flow

Users can register for events through the main portal:

1. **Register Account**
   - Endpoint: `POST /register`
   - Required fields: `username`, `email`, `password`, `first_name`, `last_name`

2. **Login to Portal**
   - Endpoint: `POST /login`
   - Required fields: `username`, `password`

3. **Buy Ticket / Register for Event**
   - Endpoint: `POST /buy-ticket`
   - Required fields: `user_id`, `event_id`
   - Returns: ticket code

4. **Check-in at Event**
   - Endpoint: `POST /check-in`
   - Required field: `ticket_code`

### API Endpoints

#### User Registration
```bash
POST http://localhost:3003/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### User Login
```bash
POST http://localhost:3003/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password"
}
```

#### Buy Ticket
```bash
POST http://localhost:3003/buy-ticket
Content-Type: application/json

{
  "user_id": 2,
  "event_id": 1
}
```

#### Check-in
```bash
POST http://localhost:3003/check-in
Content-Type: application/json

{
  "ticket_code": "A1B2C3D4E5F6"
}
```

### Testing with curl

**Test 1: Register a new user**
```bash
curl -X POST http://localhost:3003/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Test 2: User Login**
```bash
curl -X POST http://localhost:3003/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

**Test 3: Buy a Ticket** (use event_id from admin dashboard)
```bash
curl -X POST http://localhost:3003/buy-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "event_id": 1
  }'
```

---

## 📊 How Dashboard Reflects Database Changes

### When Database is Empty (Initially)
- All stat cards show **0**
- "No data" appears in charts
- Recent registrations list is empty

### After User Registers and Buys Ticket
1. **Total Registrations** increases by 1
2. **Total Users** increases by 1
3. Chart updates to show registrations per event
4. Recent registrations list shows the new user
5. User distribution chart shows 1 registered, 0 attended

### After Check-in
1. **Tickets Bought** increases by 1
2. **Attended** count in distribution chart increases
3. Recent registrations badge changes to "Verified"

### Data Refresh
- Dashboard automatically refreshes every 30 seconds
- Manual refresh: Press F5 or click refresh button

---

## 🐛 Troubleshooting

### Issue: "Database connection failed" error

**Solution:**
1. Make sure XAMPP MySQL is running
2. Verify database was initialized properly in phpMyAdmin
3. Check database name is `sd-wad-main`
4. Verify connection settings in `admin_service.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'root',
       'password': '',
       'database': 'sd-wad-main',
       'port': 3306
   }
   ```

### Issue: "Cannot reach admin service"

**Solution:**
1. Make sure `admin_service.py` is running on port 3003
2. Check if port 3003 is not blocked by firewall
3. Verify you're using correct URL: `http://localhost:3003`

### Issue: Admin login not working

**Solution:**
1. Verify admin user exists in database:
   - Go to phpMyAdmin → users table
   - Check if user with username "admin" exists
2. Password should be stored as hash (first 100 chars: `$2y$10$sVIkNg...`)
3. Make sure admin role is set to 'admin' not 'user'

### Issue: Charts show as blank/white

**Solution:**
1. Wait for data to load (may take a few seconds)
2. Press F5 to refresh page
3. Check browser console for errors (F12 → Console)
4. Verify Chart.js is loaded: Check if `<script src="...chart.js...">` is in admin-dashboard.html

### Issue: Registrations not appearing in dashboard

**Solution:**
1. Make sure ticket was purchased successfully (check curl response)
2. Wait 30 seconds for dashboard to auto-refresh
3. Click F5 to manually refresh
4. Check database directly:
   ```sql
   SELECT * FROM registrations;
   SELECT * FROM users WHERE role = 'user';
   ```

### Issue: Users table shows as empty

**Solution:**
1. Check that database initialization completed successfully
2. Verify the SQL script was executed in phpMyAdmin
3. Re-run `database-init.sql` if needed

---

## 📱 Complete User Journey Example

### Step-by-Step Test Scenario

1. **Initialize Database**
   - Run `database-init.sql` in phpMyAdmin
   - Dashboard now shows all 0s

2. **Create Event** (via admin)
   - Dashboard shows 1 total event

3. **Register User**
   ```bash
   curl -X POST http://localhost:3003/register \
     -H "Content-Type: application/json" \
     -d '{"username": "alice", "email": "alice@test.com", "password": "pass123", "first_name": "Alice", "last_name": "Smith"}'
   ```
   - Dashboard shows 1 total user

4. **User Buys Ticket**
   ```bash
   curl -X POST http://localhost:3003/buy-ticket \
     -H "Content-Type: application/json" \
     -d '{"user_id": 2, "event_id": 1}'
   ```
   - Dashboard shows 1 registration
   - Chart shows 1 registration for that event
   - Alice appears in recent registrations

5. **Admin Checks In User**
   ```bash
   curl -X POST http://localhost:3003/check-in \
     -H "Content-Type: application/json" \
     -d '{"ticket_code": "RETURNED_FROM_BUY_TICKET"}'
   ```
   - Dashboard shows 1 ticket bought
   - Distribution chart shows 1 attended, 0 pending
   - Alice's badge changes to "Verified"

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review browser console (F12) for error messages
3. Check terminal where `admin_service.py` is running for backend errors
4. Verify all services are running: admin_service.py and XAMPP MySQL

---

## 🔄 Quick Start Checklist

- [ ] XAMPP MySQL running
- [ ] Database initialized (database-init.sql executed)
- [ ] admin_service.py running on port 3003
- [ ] Admin dashboard accessible at http://localhost/path/to/admin-login.html
- [ ] Can login with admin/admin123
- [ ] Can see dashboard with all stats showing 0
- [ ] Registered test user
- [ ] Purchased test ticket
- [ ] Dashboard now shows 1 registration
- [ ] Check-in successful
- [ ] Dashboard shows 1 ticket bought

**Ready to go! 🎉**
