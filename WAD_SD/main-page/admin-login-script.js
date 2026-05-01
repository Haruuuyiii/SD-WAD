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

  const username   = document.getElementById('username').value.trim();
  const password   = document.getElementById('password').value;
  const messageDiv = document.getElementById('loginMessage');

  messageDiv.textContent = '';
  messageDiv.classList.remove('error', 'success');

  if (!username || !password) {
    showMessage('Please fill in all fields', 'error');
    return;
  }

  const loginBtn    = document.querySelector('.login-btn');
  const originalHTML = loginBtn.innerHTML;
  loginBtn.innerHTML = '<span>Logging in...</span>';
  loginBtn.disabled  = true;

  try {
    const response = await fetch('http://localhost:3003/admin/login', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok && data.role === 'admin') {
      // Store admin session
      localStorage.setItem('adminToken',    data.token);
      localStorage.setItem('adminUsername', data.username);
      localStorage.setItem('adminUserId',   data.user_id);

      showMessage('Login successful! Redirecting...', 'success');
      setTimeout(() => {
        window.location.href = './admin-dashboard.html';
      }, 1500);

    } else if (response.ok && data.role !== 'admin') {
      // Logged in but not an admin
      showMessage('Access denied: admin privileges required.', 'error');
      loginBtn.innerHTML = originalHTML;
      loginBtn.disabled  = false;

    } else {
      showMessage(data.error || 'Invalid admin credentials', 'error');
      loginBtn.innerHTML = originalHTML;
      loginBtn.disabled  = false;
    }

  } catch (error) {
    console.error('Login error:', error);
    showMessage(
      'Cannot reach admin service. Make sure admin_service.py is running on port 3003.',
      'error'
    );
    loginBtn.innerHTML = originalHTML;
    loginBtn.disabled  = false;
  }
});

function showMessage(message, type) {
  const messageDiv = document.getElementById('loginMessage');
  messageDiv.textContent = message;
  messageDiv.classList.remove('error', 'success');
  messageDiv.classList.add(type);
}

// Redirect if already logged in
window.addEventListener('load', () => {
  const adminToken = localStorage.getItem('adminToken');
  if (adminToken) {
    window.location.href = './admin-dashboard.html';
  }
});