// ─────────────────────────────────────────────────────────────
// CozMoz — script.js
// Connects the frontend to the Python gateway (port 3000)
// ─────────────────────────────────────────────────────────────

const GATEWAY = "http://localhost:3000"; // your gateway URL

// ── DOM Elements ──────────────────────────────────────────────
const loginBtn   = document.getElementById("loginBtn");
const loginPopup = document.getElementById("loginPopup");
const overlay    = document.getElementById("overlay");
const closeBtn   = document.getElementById("closeBtn");

// ── Open / Close Login Popup ──────────────────────────────────
loginBtn.addEventListener("click", (e) => {
  e.preventDefault();
  loginPopup.style.display = "block";
  overlay.style.display    = "block";
  document.body.classList.add("modal-open");
});

closeBtn.addEventListener("click", closeModal);
overlay.addEventListener("click", closeModal);

function closeModal() {
  loginPopup.style.display = "none";
  overlay.style.display    = "none";
  document.body.classList.remove("modal-open");
  clearError();
}

// ── Login Form Submit ─────────────────────────────────────────
const loginForm = document.querySelector(".login-popup form");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // stop page from reloading

  const username = loginForm.querySelector("input[type='text']").value.trim();
  const password = loginForm.querySelector("input[type='password']").value;

  if (!username || !password) {
    showError("Please fill in all fields.");
    return;
  }

  const submitBtn = loginForm.querySelector(".submit");
  submitBtn.textContent = "Logging in...";
  submitBtn.disabled    = true;

  try {
    const response = await fetch(`${GATEWAY}/api/auth/login`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      // Save token and username to localStorage
      localStorage.setItem("token",    data.token);
      localStorage.setItem("username", data.username || username);
      localStorage.setItem("role",     data.role || "user");

      showSuccess(`Welcome back, ${username}!`);

      // Send a welcome notification (calls notif_service via gateway)
      sendWelcomeNotification(username);

      // Close popup after 1.2 seconds
      setTimeout(() => {
        closeModal();
        updateNavAfterLogin(username);
      }, 1200);

    } else {
      showError(data.error || "Login failed. Please try again.");
    }

  } catch (err) {
    showError("Cannot reach the server. Make sure gateway.py is running.");
    console.error("Login error:", err);
  } finally {
    submitBtn.textContent = "Login";
    submitBtn.disabled    = false;
  }
});

// ── Update navbar after login ─────────────────────────────────
function updateNavAfterLogin(username) {
  const loginLink = document.getElementById("loginBtn");
  if (loginLink) {
    loginLink.textContent = `Hi, ${username}`;
    loginLink.style.color = "#F375C2";
    loginLink.removeEventListener("click", openModal);
    loginLink.addEventListener("click", (e) => {
      e.preventDefault();
      logout();
    });
  }
}

// ── Logout ────────────────────────────────────────────────────
async function logout() {
  const token = localStorage.getItem("token");
  if (!token) return;

  try {
    await fetch(`${GATEWAY}/api/auth/logout`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ token }),
    });
  } catch (_) {}

  localStorage.removeItem("token");
  localStorage.removeItem("username");
  localStorage.removeItem("role");
  location.reload();
}

// ── Send welcome notification via gateway → notif_service ─────
async function sendWelcomeNotification(username) {
  try {
    await fetch(`${GATEWAY}/api/notif/send`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        type:    "email",
        to:      `${username}@cozmoz.com`,
        subject: "Welcome to CozMoz!",
        message: `Hey ${username}, welcome to CozMoz! 🎉`,
      }),
    });
  } catch (_) {
    // Notification failing shouldn't break the login flow
  }
}

// ── Error / Success message helpers ──────────────────────────
function showError(msg) {
  clearError();
  const div = document.createElement("div");
  div.id    = "login-error";
  div.style.cssText = `
    color: #ff6b6b;
    font-family: Onest;
    font-size: 1.6rem;
    margin-top: 1rem;
    text-align: center;
  `;
  div.textContent = msg;
  loginForm.appendChild(div);
}

function showSuccess(msg) {
  clearError();
  const div = document.createElement("div");
  div.id    = "login-error";
  div.style.cssText = `
    color: #4dd4a8;
    font-family: Onest;
    font-size: 1.6rem;
    margin-top: 1rem;
    text-align: center;
  `;
  div.textContent = msg;
  loginForm.appendChild(div);
}

function clearError() {
  const existing = document.getElementById("login-error");
  if (existing) existing.remove();
}

// ── On page load: check if already logged in ─────────────────
window.addEventListener("load", () => {
  const username = localStorage.getItem("username");
  const token    = localStorage.getItem("token");
  if (username && token) {
    updateNavAfterLogin(username);
  }
});