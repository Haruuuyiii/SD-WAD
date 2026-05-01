# CozMoz API Endpoints Reference

## 🌐 Base URL
```
http://localhost:3003
```

---

## 🔐 Authentication Endpoints

### Admin Login
```
POST /admin/login
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}

Response (200):
{
  "message": "Welcome Admin User!",
  "token": "abc123...",
  "username": "admin",
  "user_id": 1,
  "role": "admin"
}
```

### User Registration
```
POST /register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123",
  "first_name": "John",
  "last_name": "Doe"
}

Response (201):
{
  "message": "Account created successfully! Welcome John!",
  "user_id": 2,
  "username": "john_doe"
}
```

### User Login
```
POST /login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure123"
}

Response (200):
{
  "message": "Welcome John!",
  "token": "def456...",
  "user_id": 2,
  "username": "john_doe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}
```

---

## 📊 Dashboard & Statistics Endpoints

### Get Dashboard Statistics
```
GET /dashboard/stats

Response (200):
{
  "totalEvents": 3,
  "totalRegistrations": 5,
  "activeEvents": 2,
  "ticketsBought": 3,
  "loggedInUsers": 2,
  "totalUsers": 10
}
```

### Get Registrations by Event
```
GET /dashboard/registrations-by-event

Response (200):
{
  "eventRegistrations": [
    {
      "name": "Tech Conference 2025",
      "registrations": 5,
      "color": "#3b82f6"
    },
    {
      "name": "Web Development Workshop",
      "registrations": 2,
      "color": "#f97316"
    }
  ]
}
```

### Get User Distribution
```
GET /dashboard/user-distribution

Response (200):
{
  "userDistribution": {
    "registered": 5,
    "attended": 3,
    "pending": 2
  }
}
```

### Get Recent Registrations
```
GET /dashboard/recent-registrations

Response (200):
{
  "recentRegistrations": [
    {
      "name": "John Doe",
      "initials": "JD",
      "event": "Tech Conference 2025",
      "time": "2 minutes ago",
      "badge": "verified",
      "badge_text": "Verified"
    }
  ]
}
```

### Get All Events
```
GET /dashboard/events

Response (200):
{
  "events": [
    {
      "event_id": 1,
      "event_name": "Tech Conference 2025",
      "event_description": "...",
      "event_start": "2025-05-31T10:00:00",
      "event_end": "2025-06-01T18:00:00",
      "location": "Manila Convention Center",
      "total_registrations": 5
    }
  ]
}
```

### Get All Registrations
```
GET /dashboard/registrations

Response (200):
{
  "registrations": [
    {
      "registration_id": 1,
      "user_id": 2,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "event_name": "Tech Conference 2025",
      "created_at": "2025-05-15T10:30:00",
      "checked_in": true,
      "status": "checked_in"
    }
  ]
}
```

### Get Attendance Data
```
GET /dashboard/attendance

Response (200):
{
  "attendance": [
    {
      "event_name": "Tech Conference 2025",
      "total_registered": 5,
      "attended": 4,
      "attendance_rate": 80.00
    }
  ]
}
```

---

## 🎫 Event & Ticket Management

### Get Available Events
```
GET /events

Response (200):
{
  "events": [
    {
      "event_id": 1,
      "event_name": "Tech Conference 2025",
      "event_description": "Annual technology conference...",
      "event_start": "2025-05-31T10:00:00",
      "event_end": "2025-06-01T18:00:00",
      "location": "Manila Convention Center",
      "ticket_price": 1500.00,
      "max_capacity": 500,
      "registered_count": 5,
      "spots_available": 495
    }
  ]
}
```

### Register for Event
```
POST /register-event
Content-Type: application/json

{
  "user_id": 2,
  "event_id": 1,
  "amount_paid": 1500.00
}

Response (201):
{
  "message": "Successfully registered for Tech Conference 2025!",
  "registration_id": 5,
  "ticket_code": "A1B2C3D4E5F6",
  "amount_paid": 1500.00
}
```

### Buy Ticket
```
POST /buy-ticket
Content-Type: application/json

{
  "user_id": 2,
  "event_id": 1,
  "payment_method": "card"
}

Response (201):
{
  "message": "Ticket purchased successfully for Tech Conference 2025!",
  "ticket_code": "A1B2C3D4E5F6",
  "event_name": "Tech Conference 2025",
  "price": 1500.00,
  "registration_id": 5
}
```

### Check In
```
POST /check-in
Content-Type: application/json

{
  "ticket_code": "A1B2C3D4E5F6"
}

Response (200):
{
  "message": "Successfully checked in John Doe!",
  "attendee_name": "John Doe",
  "event_name": "Tech Conference 2025",
  "check_in_time": "2025-05-31T10:15:00"
}
```

---

## ✅ Health Check

### Service Health
```
GET /health

Response (200):
{
  "service": "admin",
  "status": "ok",
  "database": "connected"
}
```

---

## ❌ Error Responses

### 400 Bad Request
```json
{
  "error": "All fields are required"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "error": "Event not found"
}
```

### 409 Conflict
```json
{
  "error": "Username or email already exists"
}
```

### 500 Server Error
```json
{
  "error": "Database connection failed"
}
```

---

## 🧪 Testing Examples

### Using cURL

#### Test 1: Get Dashboard Stats
```bash
curl http://localhost:3003/dashboard/stats
```

#### Test 2: Register User
```bash
curl -X POST http://localhost:3003/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@test.com",
    "password": "pass123",
    "first_name": "Alice",
    "last_name": "Smith"
  }'
```

#### Test 3: Buy Ticket
```bash
curl -X POST http://localhost:3003/buy-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "event_id": 1
  }'
```

#### Test 4: Check In
```bash
curl -X POST http://localhost:3003/check-in \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_code": "A1B2C3D4E5F6"
  }'
```

### Using Postman

1. Create new collection
2. Add requests with:
   - Method: POST/GET
   - URL: http://localhost:3003/endpoint
   - Headers: Content-Type: application/json (for POST)
   - Body: Raw JSON
3. Click Send

---

## 📋 Rate Limiting & Notes

- No rate limiting in current version (add for production)
- All timestamps in ISO 8601 format
- All IDs are integers
- Prices in decimal format (XX.XX)
- Status values: pending, registered, checked_in, cancelled

---

## 🔒 Authentication Notes

- Tokens are stored in localStorage for web clients
- Sessions expire after inactivity (configurable)
- Admin and user endpoints require respective roles
- Token validation on protected endpoints

---

## 📞 Support

For API issues:
1. Check health endpoint first
2. Verify request format matches examples
3. Check response for error details
4. Review browser console (F12) for client-side errors
5. Check terminal where admin_service.py is running for backend logs

---

**All endpoints are now live and ready for integration!** 🚀
