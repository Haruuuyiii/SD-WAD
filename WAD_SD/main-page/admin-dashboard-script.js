// Charts instances
let registrationsChart = null;
let userDistributionChart = null;

// Page initialization
document.addEventListener('DOMContentLoaded', () => {
  try {
    checkAuthentication();
    loadDashboardData();
    initializeCharts();
    setupNavigation();
    document.getElementById('chartPeriod').addEventListener('change', updateCharts);
  } catch (err) {
    console.error('Admin dashboard error:', err);
    showDashboardError('Unable to load dashboard content. Check the console for details.');
  }
});

window.addEventListener('error', (event) => {
  console.error('Unhandled error:', event.error || event.message);
  showDashboardError('A runtime error occurred while loading the dashboard.');
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
  showDashboardError('A promise error occurred while loading the dashboard.');
});

function showDashboardError(message) {
  const messageDiv = document.getElementById('dashboardErrorMessage');
  if (messageDiv) {
    messageDiv.textContent = message;
    messageDiv.hidden = false;
  }
}

// Check if user is authenticated
function checkAuthentication() {
  const adminToken = localStorage.getItem('adminToken');
  const adminUsername = localStorage.getItem('adminUsername');
  
  if (!adminToken || !adminUsername) {
    // Redirect to login if not authenticated
    window.location.href = './admin-login.html';
    return;
  }
  
  // Update admin name in sidebar
  document.getElementById('adminName').textContent = adminUsername;
}

// Load dashboard data
function loadDashboardData() {
  // Sample data - Replace with actual API calls
  const dashboardData = {
    totalEvents: 6,
    totalRegistrations: 13,
    activeEvents: 6,
    ticketsBought: 4,
    loggedInUsers: 8,
    totalUsers: 24,
    eventRegistrations: [
      { name: 'TechTalk 2024', registrations: 4, color: '#3b82f6' },
      { name: 'Web Dev Workshop', registrations: 3, color: '#f97316' },
      { name: 'Design Bootcamp', registrations: 3, color: '#06b6d4' },
      { name: 'AI Summit', registrations: 2, color: '#8b5cf6' },
      { name: 'Mobile Dev Conference', registrations: 1, color: '#ec4899' }
    ],
    userDistribution: {
      registered: 13,
      attended: 4,
      pending: 7
    }
  };
  
  // Update stat cards
  document.getElementById('totalEvents').textContent = dashboardData.totalEvents;
  document.getElementById('totalRegistrations').textContent = dashboardData.totalRegistrations;
  document.getElementById('activeEvents').textContent = dashboardData.activeEvents;
  document.getElementById('ticketsBought').textContent = dashboardData.ticketsBought;
  document.getElementById('loggedInUsers').textContent = dashboardData.loggedInUsers;
  document.getElementById('totalUsers').textContent = dashboardData.totalUsers;
  
  // Store for chart initialization
  window.dashboardData = dashboardData;
}

// Initialize charts
function initializeCharts() {
  if (!window.dashboardData) return;
  
  // Registrations Chart
  const registrationsCtx = document.getElementById('registrationsChart');
  if (registrationsCtx) {
    if (registrationsChart) {
      registrationsChart.destroy();
    }
    
    registrationsChart = new Chart(registrationsCtx, {
      type: 'bar',
      data: {
        labels: window.dashboardData.eventRegistrations.map(e => e.name),
        datasets: [{
          label: 'Registrations',
          data: window.dashboardData.eventRegistrations.map(e => e.registrations),
          backgroundColor: window.dashboardData.eventRegistrations.map(e => e.color),
          borderRadius: 8,
          borderSkipped: false,
          hoverBackgroundColor: '#6366f1'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            borderRadius: 8,
            titleFont: {
              size: 13,
              weight: 'bold'
            },
            bodyFont: {
              size: 12
            },
            displayColors: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 5,
            ticks: {
              stepSize: 1,
              font: {
                size: 12
              },
              color: '#9ca3af'
            },
            grid: {
              color: '#e5e7eb',
              drawBorder: false
            }
          },
          x: {
            ticks: {
              font: {
                size: 12
              },
              color: '#6b7280'
            },
            grid: {
              display: false
            }
          }
        }
      }
    });
  }
  
  // User Distribution Chart
  const userDistributionCtx = document.getElementById('userDistributionChart');
  if (userDistributionCtx) {
    if (userDistributionChart) {
      userDistributionChart.destroy();
    }
    
    userDistributionChart = new Chart(userDistributionCtx, {
      type: 'doughnut',
      data: {
        labels: ['Registered', 'Attended', 'Pending'],
        datasets: [{
          data: [
            window.dashboardData.userDistribution.registered,
            window.dashboardData.userDistribution.attended,
            window.dashboardData.userDistribution.pending
          ],
          backgroundColor: [
            '#10b981',
            '#3b82f6',
            '#f59e0b'
          ],
          borderWidth: 2,
          borderColor: 'white',
          hoverBorderColor: '#6b7280'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              font: {
                size: 12
              },
              color: '#6b7280',
              padding: 15,
              usePointStyle: true,
              pointStyle: 'circle'
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            borderRadius: 8,
            titleFont: {
              size: 13,
              weight: 'bold'
            },
            bodyFont: {
              size: 12
            },
            displayColors: true,
            callbacks: {
              label: function(context) {
                return context.label + ': ' + context.parsed + ' users';
              }
            }
          }
        }
      }
    });
  }
}

// Update charts based on selected period
function updateCharts() {
  const period = document.getElementById('chartPeriod').value;
  
  // Update data based on period (this is just a demo)
  const periodData = {
    week: [2, 1, 1, 0, 0],
    month: [4, 3, 3, 2, 1],
    year: [10, 8, 12, 6, 5]
  };
  
  if (registrationsChart && periodData[period]) {
    registrationsChart.data.datasets[0].data = periodData[period];
    registrationsChart.update();
  }
}

// Setup page navigation
function setupNavigation() {
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      
      const page = link.getAttribute('data-page');
      navigateToPage(page);
      
      // Update active nav item
      document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
      });
      link.closest('.nav-item').classList.add('active');
    });
  });
}

// Navigate to page
function navigateToPage(page) {
  // Hide all pages
  document.querySelectorAll('.page').forEach(p => {
    p.classList.remove('active');
  });
  
  // Show selected page
  const selectedPage = document.getElementById(`${page}-page`);
  if (selectedPage) {
    selectedPage.classList.add('active');
  }
  
  // Update page title and subtitle
  const titles = {
    dashboard: { title: 'Dashboard', subtitle: 'Welcome back to CozMoz Admin Panel' },
    events: { title: 'Events', subtitle: 'Manage all your events' },
    registrations: { title: 'Registrations', subtitle: 'View all event registrations' },
    attendance: { title: 'Attendance', subtitle: 'Track event attendance' },
    analytics: { title: 'Analytics', subtitle: 'Detailed analytics and insights' },
    announcements: { title: 'Announcements', subtitle: 'Create and manage announcements' }
  };
  
  if (titles[page]) {
    document.getElementById('pageTitle').textContent = titles[page].title;
    document.getElementById('pageSubtitle').textContent = titles[page].subtitle;
  }
  
  // Reinitialize charts if on dashboard
  if (page === 'dashboard') {
    setTimeout(() => {
      initializeCharts();
    }, 100);
  }
}

// Logout function
function logout() {
  if (confirm('Are you sure you want to logout?')) {
    localStorage.removeItem('adminToken');
    localStorage.removeItem('adminUsername');
    window.location.href = './admin-login.html';
  }
}

// Auto-refresh data every 30 seconds
setInterval(() => {
  loadDashboardData();
}, 30000);

// Prevent going back to login after logout
window.addEventListener('pageshow', (event) => {
  if (event.persisted) {
    checkAuthentication();
  }
});
