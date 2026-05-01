# CozMoz Admin Panel Documentation

## Overview
The CozMoz Admin Panel is a comprehensive management system for tracking events, registrations, and user activity. It provides real-time statistics, analytics, and administrative controls.

## Files Created

### 1. **admin-login.html**
   - Admin authentication page
   - Location: `/main-page/admin-login.html`
   - Features:
     - Modern gradient design
     - Username/Password login form
     - Remember me functionality
     - Password visibility toggle
     - Responsive design

### 2. **admin-login-style.css**
   - Styling for the admin login page
   - Location: `/main-page/admin-login-style.css`
   - Features:
     - Professional gradient backgrounds
     - Smooth animations and transitions
     - Mobile responsive layout
     - Accessibility optimized

### 3. **admin-login-script.js**
   - Login functionality and authentication
   - Location: `/main-page/admin-login-script.js`
   - Features:
     - Form validation
     - API connection to auth service
     - Session management with localStorage
     - Automatic redirect to dashboard

### 4. **admin-dashboard.html**
   - Main admin dashboard interface
   - Location: `/main-page/admin-dashboard.html`
   - Features:
     - Sidebar navigation
     - Statistics cards showing:
       - Total Events: 6
       - Total Registrations: 13
       - Active Events: 6
       - Tickets Bought/Checked: 4
       - Logged In Users: 8
       - Total Users: 24
     - Interactive charts (Bar & Doughnut)
     - Recent registrations list
     - Multi-page navigation

### 5. **admin-dashboard-style.css**
   - Complete styling for dashboard
   - Location: `/main-page/admin-dashboard-style.css`
   - Features:
     - Modern UI with CSS Grid
     - Dark/Light theme support
     - Responsive layouts
     - Animation effects
     - Custom scrollbar styling

### 6. **admin-dashboard-script.js**
   - Dashboard functionality and interactions
   - Location: `/main-page/admin-dashboard-script.js`
   - Features:
     - Chart initialization with Chart.js
     - Page navigation
     - Data loading and updates
     - Auto-refresh every 30 seconds
     - Authentication verification

## Access Instructions

### From Home Page
1. Click the **ADMIN** button in the navigation menu
2. You'll be directed to the admin login page

### Login Credentials
**Default Admin Account:**
- **Username:** admin
- **Password:** 1234

**Note:** Update these credentials in `page2/auth_service.py` for production use.

## Features

### Dashboard Statistics
The dashboard displays 6 key metrics:
- **Total Events:** 6 - All events in the system
- **Total Registrations:** 13 - Total user registrations
- **Active Events:** 6 - Currently active events
- **Tickets Bought/Checked:** 4 - Attendance tracking
- **Logged In Users:** 8 - Current active users
- **Total Users:** 24 - Total registered users

### Charts & Analytics
1. **Registrations per Event** (Bar Chart)
   - Shows registration counts for each event
   - Filterable by time period (Week/Month/Year)
   - Color-coded events

2. **User Distribution** (Doughnut Chart)
   - Registered: 13 users
   - Attended: 4 users
   - Pending: 7 users

### Recent Registrations
Displays the latest user registrations with:
- User name
- Event they registered for
- Registration time
- Verification status

### Navigation Menu
- **Dashboard** - Overview and statistics
- **Events** - Event management (Coming Soon)
- **Registrations** - View all registrations (Coming Soon)
- **Attendance** - Track attendance (Coming Soon)
- **Analytics** - Detailed analytics (Coming Soon)
- **Announcements** - Post announcements (Coming Soon)

## Security Features

### Authentication
- Session-based login using localStorage
- Token validation on page load
- Automatic redirect if not authenticated
- Logout with confirmation dialog

### Session Management
- Admin token stored in localStorage
- Auto-verification on page load
- Session persistence across page reloads

## Integration Points

### Backend Services
The admin panel integrates with:
1. **Auth Service** (`port 5000`)
   - `/login` - Authenticate admin
   - Role-based access control

2. **User Service** (`port 3002`)
   - User profile data
   - User statistics

### Database
Currently uses mock data. To integrate with real database:
1. Update `admin-dashboard-script.js` `loadDashboardData()` function
2. Replace mock data with API calls
3. Connect to your MySQL/PostgreSQL backend

## Customization

### Adding Statistics
Edit `loadDashboardData()` in `admin-dashboard-script.js`:
```javascript
const dashboardData = {
  totalEvents: 6,
  totalRegistrations: 13,
  // Add more metrics here
};
```

### Adding New Pages
1. Add navigation item in `admin-dashboard.html`
2. Create corresponding page div with class "page"
3. Add page title in navigation

### Changing Colors
Update CSS variables in `admin-dashboard-style.css`:
```css
:root {
  --primary: #6366f1;
  --secondary: #ec4899;
  --success: #10b981;
  /* ... more colors */
}
```

## Responsive Design

The admin panel is fully responsive:
- **Desktop:** Full sidebar + content layout
- **Tablet:** Collapsed sidebar with toggle
- **Mobile:** Hamburger menu navigation

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- Charts use Chart.js v4.4.0 for efficient rendering
- Auto-refresh every 30 seconds
- Lazy loading of charts on page navigation
- Optimized CSS animations

## Future Enhancements

1. Real-time data updates with WebSocket
2. Export reports to PDF/Excel
3. Advanced filtering and search
4. User role management
5. Email notifications
6. API documentation
7. Dark mode toggle
8. Multi-language support

## Troubleshooting

### Login Issues
- Check if auth service is running on port 5000
- Verify credentials in `page2/auth_service.py`
- Clear browser cache and localStorage

### Charts Not Displaying
- Ensure Chart.js CDN is accessible
- Check browser console for errors
- Verify canvas elements exist in HTML

### No Data Showing
- Verify API endpoints are responding
- Check network tab in browser dev tools
- Ensure cors are properly configured

## Contact & Support
For issues or features requests, please update the backend services or contact the development team.