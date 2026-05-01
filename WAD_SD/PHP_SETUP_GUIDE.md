# CozMoz - PHP-Based Setup Guide

## 🚀 Setup Using PHP (Instead of Python)

This guide uses PHP for database initialization and API endpoints instead of the Python service.

---

## 📋 Prerequisites

- XAMPP with MySQL and PHP
- PHP 7.4 or higher
- MySQL 5.7 or higher
- VS Code or text editor

---

## 🔧 Step 1: Initialize Database Using PHP

### Option A: Using Browser (Recommended)

1. **Start XAMPP**
   - Open XAMPP Control Panel
   - Click "Start" next to Apache and MySQL

2. **Access the initialization script**
   - URL: `http://localhost/path/to/page2/database-init.php`
   - The script will create all tables and insert default data
   - You'll see colored output showing success/errors

**Expected Output:**
```
═══════════════════════════════════════════════════════════════
  CozMoz Event Management System - Database Initialization
═══════════════════════════════════════════════════════════════

[1] Creating USERS table...
✓ USERS table created successfully
[2] Creating EVENTS table...
✓ EVENTS table created successfully
[3] Creating REGISTRATIONS table...
✓ REGISTRATIONS table created successfully
...
```

### Option B: Using Command Line

```bash
cd page2
php database-init.php
```

---

## 🌐 Step 2: Set Up PHP API Endpoints

The `api.php` file provides all the same functionality as the Python service.

### API Base URL (via PHP)
```
http://localhost/path/to/page2/api.php
```

### Making API Calls

All endpoints work the same as the Python version but route through `api.php`:

**Example: Get Dashboard Stats**
```bash
curl http://localhost/path/to/page2/api.php?action=dashboard/stats
```

Or with POST:
```bash
curl -X POST http://localhost/path/to/page2/api.php \
  -H "Content-Type: application/json" \
  -d '{"action":"admin/login", "username":"admin", "password":"admin123"}'
```

---

## 📊 Available PHP API Endpoints

### Health Check
```
GET /api.php?action=health
```

### Admin Authentication
```
POST /api.php
{
  "action": "admin/login",
  "username": "admin",
  "password": "admin123"
}
```

### User Registration
```
POST /api.php
{
  "action": "register",
  "username": "john",
  "email": "john@test.com",
  "password": "pass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### Dashboard Statistics
```
GET /api.php?action=dashboard/stats
```

### All Other Endpoints
All endpoints from the Python service are available:
- `dashboard/registrations-by-event`
- `dashboard/user-distribution`
- `dashboard/recent-registrations`
- `buy-ticket`
- `check-in`
- `events`
- And more...

---

## 🔐 Configure Admin Dashboard to Use PHP API

Update `admin-dashboard-script.js` to use PHP endpoints:

### Change 1: Update Dashboard Stats Endpoint
```javascript
// OLD (Python)
fetch('http://localhost:3003/dashboard/stats')

// NEW (PHP)
fetch('http://localhost/path/to/page2/api.php?action=dashboard/stats')
```

### Change 2: Update Admin Login Script
In `admin-login-script.js`:
```javascript
// OLD
fetch('http://localhost:3003/admin/login', {

// NEW
fetch('http://localhost/path/to/page2/api.php', {
  body: JSON.stringify({
    action: 'admin/login',
    username: username,
    password: password
  })
})
```

---

## 🧪 Testing PHP API

### Test 1: Health Check
```bash
curl http://localhost/path/to/page2/api.php?action=health
```

### Test 2: Get Dashboard Stats
```bash
curl "http://localhost/path/to/page2/api.php?action=dashboard/stats"
```

### Test 3: Register User
```bash
curl -X POST http://localhost/path/to/page2/api.php \
  -H "Content-Type: application/json" \
  -d '{
    "action": "register",
    "username": "testuser",
    "email": "test@example.com",
    "password": "pass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Test 4: Admin Login
```bash
curl -X POST http://localhost/path/to/page2/api.php \
  -H "Content-Type: application/json" \
  -d '{
    "action": "admin/login",
    "username": "admin",
    "password": "admin123"
  }'
```

### Test 5: Buy Ticket
```bash
curl -X POST http://localhost/path/to/page2/api.php \
  -H "Content-Type: application/json" \
  -d '{
    "action": "buy-ticket",
    "user_id": 2,
    "event_id": 1
  }'
```

---

## 📁 File Structure

```
page2/
├── connect.php                    (Existing database connection)
├── database-init.php             (NEW - Database setup with PHP)
├── api.php                        (NEW - All API endpoints in PHP)
├── login.php                      (User login)
├── sign_up.php                    (User registration)
└── requirements.txt               (For Python dependencies, if using Python)
```

---

## 🚀 Quick Setup Checklist

- [ ] Start XAMPP (Apache + MySQL)
- [ ] Run `http://localhost/path/to/page2/database-init.php`
- [ ] Verify tables created in phpMyAdmin
- [ ] Access admin dashboard: `http://localhost/path/to/admin-login.html`
- [ ] Login: `admin` / `admin123`
- [ ] See dashboard with all 0s (database is empty)
- [ ] Register user via curl
- [ ] Dashboard stats update automatically

---

## 🔄 Choosing Between Python and PHP

### Use Python Service (`admin_service.py`) If:
- You want standalone API service
- You need background tasks/scheduling
- You prefer Flask over PHP
- You want asynchronous operations

### Use PHP API (`api.php`) If:
- You want everything in PHP
- Simpler deployment (just drop in XAMPP)
- Already built with PHP
- No need for standalone service
- Easier to host on shared PHP hosting

---

## 🔀 Using Both Simultaneously

You can run **both** Python and PHP APIs at the same time:

1. **PHP** handles user-facing features: registration, login, ticket purchase
2. **Python** handles admin dashboard and complex analytics

Just use different URLs in your frontend:
- User portal → PHP: `http://localhost/path/to/page2/api.php`
- Admin dashboard → Python: `http://localhost:3003`

---

## 📞 Troubleshooting

### "database-init.php shows errors"
- [ ] Check MySQL is running
- [ ] Verify connect.php connection works
- [ ] Check file permissions on page2 folder

### "API endpoints return 404"
- [ ] Verify correct URL path
- [ ] Check Apache is serving PHP files
- [ ] Test: `http://localhost/path/to/page2/api.php?action=health`

### "Database tables not created"
- [ ] Run database-init.php again
- [ ] Check phpMyAdmin to verify database exists
- [ ] Check error messages in browser

### "Admin login fails"
- [ ] Verify admin user was created (check phpMyAdmin)
- [ ] Verify password is: `admin123`
- [ ] Check user table has admin role

---

## 🎯 Next Steps

1. **Run database initialization**: Access `database-init.php` in browser
2. **Test API**: Use curl commands above
3. **Update dashboard**: Point to PHP API endpoints
4. **Register users**: Test user registration
5. **Buy tickets**: Verify dashboard stats update
6. **Check in**: Test attendance tracking

---

## 📚 Additional Resources

- `API_REFERENCE.md` - All endpoint documentation
- `connect.php` - Database connection settings
- `phpMyAdmin` - View and manage database tables

---

## ✨ You're Now Using PHP-Based Setup!

All the functionality of the Python service is now available via PHP. Your admin dashboard will show:

✅ **0** for all metrics when database is empty
✅ **Real-time updates** as users register and buy tickets
✅ **Charts** that fill with data
✅ **Recent registrations** as they happen
✅ **Attendance tracking** when users check in

**Ready to go!** 🚀
