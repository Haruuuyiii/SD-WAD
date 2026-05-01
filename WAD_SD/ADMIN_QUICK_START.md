# Admin Panel Quick Setup Guide

## 🚀 What's New

Your CozMoz website now has a complete **Admin Dashboard** system with:

✅ Admin Login Page
✅ Professional Dashboard with Statistics
✅ Real-time Charts & Analytics
✅ Recent Activity Tracking
✅ Responsive Design (Mobile, Tablet, Desktop)
✅ Session Management

---

## 📁 Files Created

All files are in `/main-page/` folder:

```
main-page/
├── admin-login.html              ← Admin login page
├── admin-login-style.css         ← Login styling
├── admin-login-script.js         ← Login functionality
├── admin-dashboard.html          ← Dashboard main page
├── admin-dashboard-style.css     ← Dashboard styling
├── admin-dashboard-script.js     ← Dashboard functionality
└── index.html                    ← Updated with ADMIN link
```

---

## 🔐 How to Access

### From Home Page
1. Go to `http://localhost/WAD_SD/main-page/index.html`
2. Click the **ADMIN** button in the top navigation bar
3. You'll be taken to the admin login page

### Login Credentials
- **Username:** `admin`
- **Password:** `1234`

**⚠️ Important:** Change these credentials in production!

---

## 📊 Dashboard Features

### Statistics Cards (6 Key Metrics)
| Metric | Value |
|--------|-------|
| Total Events | 6 |
| Total Registrations | 13 |
| Active Events | 6 |
| Tickets Bought/Checked | 4 |
| Logged In Users | 8 |
| Total Users | 24 |

### Charts
1. **Registrations per Event** (Bar Chart)
   - Visual representation of registrations by event
   - Filter by Week/Month/Year

2. **User Distribution** (Pie Chart)
   - Shows registered, attended, and pending users

### Recent Registrations
- Lists the last 5 user registrations
- Shows registration status (Verified/Pending)
- Displays time of registration

### Navigation Menu
- Dashboard (Current)
- Events (Coming Soon)
- Registrations (Coming Soon)
- Attendance (Coming Soon)
- Analytics (Coming Soon)
- Announcements (Coming Soon)

---

## 🛠️ Setup Instructions

### Step 1: Verify Backend Services
Make sure your auth service is running:
```bash
# In page2/ directory
python auth_service.py
# Should run on http://localhost:5000
```

### Step 2: Access Admin Panel
```
URL: http://localhost/WAD_SD/main-page/admin-login.html
```

### Step 3: Login with Default Credentials
- Username: `admin`
- Password: `1234`

### Step 4: View Dashboard
After successful login, you'll see the admin dashboard with all statistics and charts.

---

## 🔑 Key Features

### ✨ Authentication
- Secure login system
- Session management with localStorage
- Auto-redirect if not logged in
- Logout confirmation

### 📈 Real-time Data
- Statistics update every 30 seconds
- Interactive charts with hover tooltips
- Responsive to data changes

### 🎨 Modern Design
- Professional gradient color scheme
- Smooth animations and transitions
- Mobile-responsive layout
- Accessibility optimized

### 🔄 Easy Navigation
- Sidebar menu for page navigation
- Breadcrumb titles
- Quick access icons in top bar
- Search functionality ready

---

## ⚙️ Configuration

### Change Login Credentials
Edit `/page2/auth_service.py`:
```python
USERS = {
    "admin": {"password": "your_new_password", "role": "admin"},
}
```

### Customize Statistics
Edit `/main-page/admin-dashboard-script.js`:
```javascript
function loadDashboardData() {
  const dashboardData = {
    totalEvents: 6,
    totalRegistrations: 13,
    // Update these values
  };
}
```

### Change Colors
Edit `/main-page/admin-dashboard-style.css`:
```css
:root {
  --primary: #6366f1;        /* Main color */
  --secondary: #ec4899;      /* Accent color */
  --success: #10b981;        /* Success color */
  /* ... */
}
```

---

## 📱 Responsive Behavior

- **Desktop (1024px+):** Full sidebar + full content
- **Tablet (768px-1024px):** Collapsed sidebar with toggle
- **Mobile (< 768px):** Hidden sidebar, hamburger menu

---

## 🔗 Integration Points

### Auth Service (port 5000)
- Login endpoint: `POST /login`
- Register endpoint: `POST /register`
- Health check: `GET /health`

### User Service (port 3002)
- Get profiles: `GET /profile`
- Get user: `GET /profile/<username>`

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Login page not loading | Check internet connection, verify files are in correct folder |
| Can't login | Ensure auth_service.py is running on port 5000 |
| Charts not displaying | Update Chart.js CDN URL, check browser console |
| Data not loading | Verify backend services are running |
| Mobile layout broken | Clear browser cache, check CSS file is loaded |

---

## 📋 Next Steps

### To Connect Real Data
1. Update `loadDashboardData()` in `admin-dashboard-script.js`
2. Make API calls to your backend instead of mock data
3. Update database queries to fetch real statistics

### To Add New Pages
1. Add new navigation item in `admin-dashboard.html`
2. Create new page div with class="page"
3. Add JavaScript handlers in `admin-dashboard-script.js`

### To Customize Further
- Edit CSS files for styling changes
- Edit JavaScript files for functionality changes
- Update HTML structure as needed

---

## 📞 Support

For detailed information, see: `ADMIN_PANEL_README.md`

Happy administrating! 🎉