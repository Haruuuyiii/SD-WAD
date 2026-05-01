// Toggle password visibility
function togglePassword() {
  const passwordInput = document.getElementById('password');
  const toggleIcon = document.querySelector('.toggle-password');
  
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    toggleIcon.classList.remove('fa-eye');
    toggleIcon.classList.add('fa-eye-slash');
  } else {
    passwordInput.type = 'password';
    toggleIcon.classList.remove('fa-eye-slash');
    toggleIcon.classList.add('fa-eye');
  }
}

// Handle login form submission
document.getElementById('adminLoginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const messageDiv = document.getElementById('loginMessage');
  
  // Clear previous messages
  messageDiv.textContent = '';
  messageDiv.classList.remove('error', 'success');
  
  if (!username || !password) {
    showMessage('Please fill in all fields', 'error');
    return;
  }
  
  try {
    // Try to login using the gateway service
    const response = await fetch('http://localhost:3000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });
    
    const data = await response.json();
    
    if (response.ok && data.role === 'admin') {
      showMessage('Login successful! Redirecting...', 'success');
      
      // Store admin token in localStorage
      localStorage.setItem('adminToken', data.token);
      localStorage.setItem('adminUsername', data.username);
      
      // Redirect to admin dashboard after 1.5 seconds
      setTimeout(() => {
        window.location.href = './admin-dashboard.html';
      }, 1500);
    } else if (response.ok && data.role !== 'admin') {
      showMessage('Access denied. Admin credentials required.', 'error');
    } else {
      showMessage(data.error || 'Invalid credentials', 'error');
    }
  } catch (error) {
    console.error('Login error:', error);
    showMessage('Cannot reach the authentication server. Start gateway.py or auth_service.py.', 'error');
  }
});

function showMessage(message, type) {
  const messageDiv = document.getElementById('loginMessage');
  messageDiv.textContent = message;
  messageDiv.classList.add(type);
}

// Check if already logged in
window.addEventListener('load', () => {
  const adminToken = localStorage.getItem('adminToken');
  if (adminToken) {
    window.location.href = './admin-dashboard.html';
  }
});
