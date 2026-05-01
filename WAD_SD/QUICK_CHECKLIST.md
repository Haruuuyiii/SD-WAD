# CozMoz - Quick Setup Checklist

## 📋 One-Time Setup

Follow these steps in order:

### Step 1: Prepare Your System
- [ ] XAMPP installed with MySQL module
- [ ] Python 3.8+ installed
- [ ] Internet connection (for downloading dependencies)

### Step 2: Initialize Database
- [ ] Open http://localhost/phpmyadmin
- [ ] Go to SQL tab
- [ ] Copy contents of `page2/database-init.sql`
- [ ] Paste and click Go
- [ ] Verify database `sd-wad-main` was created

### Step 3: Install Dependencies
```bash
cd page2
pip install -r requirements.txt
```
- [ ] All packages installed successfully

### Step 4: Start Services
Open Command Prompt/PowerShell in `page2` folder:
```bash
python admin_service.py
```
- [ ] Service starts without errors
- [ ] Shows "Running on http://127.0.0.1:3003"
- [ ] Keep this window open

---

## 🧪 Test the System

### Test 1: Verify Service is Running
```bash
curl http://localhost:3003/health
```
- [ ] Returns: `{"service": "admin", "status": "ok", "database": "connected"}`

### Test 2: Admin Login
1. Open browser: `http://localhost/path/to/admin-login.html`
2. Enter:
   - Username: `admin`
   - Password: `admin123`
- [ ] Successfully logs in
- [ ] Redirects to dashboard

### Test 3: Dashboard Shows All Zeros
- [ ] Total Events: 0
- [ ] Total Registrations: 0
- [ ] Active Events: 0
- [ ] Tickets Bought: 0
- [ ] All stats showing 0 (correct for empty database)

### Test 4: Register a User
```bash
curl -X POST http://localhost:3003/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@test.com",
    "password": "pass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```
- [ ] Returns user_id (e.g., 2)
- [ ] Verify: Dashboard now shows 1 Total User

### Test 5: Buy Ticket
```bash
curl -X POST http://localhost:3003/buy-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "event_id": 1
  }'
```
- [ ] Returns ticket_code
- [ ] Refresh dashboard
- [ ] Total Registrations increases to 1

### Test 6: Check In
```bash
curl -X POST http://localhost:3003/check-in \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_code": "RETURNED_FROM_TEST_5"
  }'
```
- [ ] Returns success message
- [ ] Refresh dashboard
- [ ] Tickets Bought increases to 1

---

## 📊 Expected Dashboard Results After Tests

| Metric | Initial | After Test 4 | After Test 5 | After Test 6 |
|--------|---------|--------------|--------------|--------------|
| Total Users | 0 | 1 | 1 | 1 |
| Total Registrations | 0 | 0 | 1 | 1 |
| Tickets Bought | 0 | 0 | 0 | 1 |
| Recent Registrations | None | None | 1 | 1 (Verified) |

---

## 🔧 Troubleshooting

### "Cannot reach admin service"
- [ ] Check admin_service.py is running
- [ ] Check Python window shows "Running on http://127.0.0.1:3003"
- [ ] Restart admin_service.py

### "Database connection failed"
- [ ] Check XAMPP MySQL is running (green indicator)
- [ ] Run database initialization again
- [ ] Verify database name is `sd-wad-main`

### Admin login fails
- [ ] Verify admin user exists in database
- [ ] Check database was initialized successfully
- [ ] Clear browser cache and try again

### Dashboard shows undefined instead of numbers
- [ ] Make sure admin_service.py is running
- [ ] Refresh page (F5)
- [ ] Check browser console for errors (F12)

---

## 🎯 Next Actions

### After Successful Testing
1. **Integrate with user registration** - Connect main portal to `/register` endpoint
2. **Add ticket purchase UI** - Allow users to buy tickets through web interface
3. **Create check-in scanner** - QR code scanner for event check-ins
4. **Set up notifications** - Email confirmations for registrations
5. **Add event creation UI** - Allow admins to create events through dashboard

### Production Checklist
- [ ] Change admin password (currently: admin123)
- [ ] Set up database backups
- [ ] Enable HTTPS
- [ ] Add input validation
- [ ] Implement rate limiting
- [ ] Set up logging
- [ ] Configure email service
- [ ] Add payment processing

---

## 📚 Documentation Files

1. **SETUP_GUIDE.md** - Comprehensive setup guide with all details
2. **IMPLEMENTATION_SUMMARY.md** - Technical overview of what's been built
3. **This file** - Quick reference checklist

---

## 🚀 You're Ready to Go!

All systems are now integrated and working. The admin dashboard will:

✅ Show **0** for all metrics when database is empty
✅ Update in **real-time** as users register and buy tickets
✅ Display **charts** that fill with data
✅ Show **recent registrations** as they happen
✅ Track **attendance** when users check in

**Start using the system now!** 🎉
