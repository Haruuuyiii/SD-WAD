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

// Load dashboard data from API
function loadDashboardData() {
  // Fetch stats from admin service
  fetch('http://localhost:3003/dashboard/stats')
    .then(response => {
      if (!response.ok) throw new Error('Failed to fetch stats');
      return response.json();
    })
    .then(stats => {
      // Update stat cards with real data
      document.getElementById('totalEvents').textContent = stats.totalEvents || 0;
      document.getElementById('totalRegistrations').textContent = stats.totalRegistrations || 0;
      document.getElementById('activeEvents').textContent = stats.activeEvents || 0;
      document.getElementById('ticketsBought').textContent = stats.ticketsBought || 0;
      document.getElementById('loggedInUsers').textContent = stats.loggedInUsers || 0;
      document.getElementById('totalUsers').textContent = stats.totalUsers || 0;
      
      // Store stats for later use
      window.dashboardStats = stats;
    })
    .catch(err => {
      console.error('Error loading stats:', err);
      showDashboardError('Failed to load dashboard statistics. Make sure admin_service.py is running.');
    });
  
  // Fetch event registrations
  fetch('http://localhost:3003/dashboard/registrations-by-event')
    .then(response => response.json())
    .then(data => {
      if (data.eventRegistrations) {
        window.eventRegistrationData = data.eventRegistrations;
      }
    })
    .catch(err => console.error('Error loading registrations by event:', err));
  
  // Fetch user distribution
  fetch('http://localhost:3003/dashboard/user-distribution')
    .then(response => response.json())
    .then(data => {
      if (data.userDistribution) {
        window.userDistributionData = data.userDistribution;
      }
    })
    .catch(err => console.error('Error loading user distribution:', err));
  
  // Fetch recent registrations
  fetch('http://localhost:3003/dashboard/recent-registrations')
    .then(response => response.json())
    .then(data => {
      if (data.recentRegistrations) {
        updateRecentRegistrations(data.recentRegistrations);
      }
    })
    .catch(err => console.error('Error loading recent registrations:', err));
}

// Update recent registrations list
function updateRecentRegistrations(registrations) {
  const recentList = document.querySelector('.recent-list');
  if (!recentList) return;
  
  recentList.innerHTML = '';
  
  registrations.forEach(reg => {
    const recentItem = document.createElement('div');
    recentItem.className = 'recent-item';
    
    const badgeClass = reg.badge === 'verified' ? 'verified' : 'pending';
    const badgeIcon = reg.badge === 'verified' ? 'fa-check' : 'fa-clock';
    
    recentItem.innerHTML = `
      <div class="recent-avatar">${reg.initials}</div>
      <div class="recent-info">
        <p class="recent-name">${reg.name}</p>
        <p class="recent-event">${reg.event}</p>
      </div>
      <p class="recent-time">Registered ${reg.time}</p>
      <span class="badge ${badgeClass}"><i class="fas ${badgeIcon}"></i> ${reg.badge_text}</span>
    `;
    
    recentList.appendChild(recentItem);
  });
}

// Initialize charts
function initializeCharts() {
  // Registrations Chart
  const registrationsCtx = document.getElementById('registrationsChart');
  if (registrationsCtx) {
    if (registrationsChart) {
      registrationsChart.destroy();
    }
    
    // Use real data if available, otherwise fallback to empty
    let chartData = window.eventRegistrationData || [];
    if (chartData.length === 0) {
      chartData = [
        { name: 'No data', registrations: 0, color: '#e5e7eb' }
      ];
    }
    
    registrationsChart = new Chart(registrationsCtx, {
      type: 'bar',
      data: {
        labels: chartData.map(e => e.name),
        datasets: [{
          label: 'Registrations',
          data: chartData.map(e => e.registrations),
          backgroundColor: chartData.map(e => e.color),
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
    
    // Use real data if available
    let distData = window.userDistributionData || {
      registered: 0,
      attended: 0,
      pending: 0
    };
    
    userDistributionChart = new Chart(userDistributionCtx, {
      type: 'doughnut',
      data: {
        labels: ['Registered', 'Attended', 'Pending'],
        datasets: [{
          data: [
            distData.registered,
            distData.attended,
            distData.pending
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
