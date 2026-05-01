from flask import Flask, request, jsonify, send_from_directory # type: ignore
from flask_cors import CORS # type: ignore
import requests # type: ignore
import time
import os

app = Flask(__name__, static_folder="static")
CORS(app)

SERVICES = {
    "auth":  "http://localhost:3000", 
    "user":  "http://localhost:3002", 
    "notif": "http://localhost:3004", 
}

rate_limit_store = {}
RATE_LIMIT = 15
RATE_WINDOW = 60

def check_rate_limit(ip):
    now = time.time()
    history = rate_limit_store.get(ip, [])
    history = [t for t in history if now - t < RATE_WINDOW]
    if len(history) >= RATE_LIMIT:
        return False
    history.append(now)
    rate_limit_store[ip] = history
    return True


active_tokens = {}  

def check_auth(req):
    auth_header = req.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        return token in active_tokens
    return False

@app.before_request
def middleware():
    ip = request.remote_addr
    public = ["/health", "/api/auth/login", "/api/auth/register", "/"]
    if request.path in public or request.path.startswith("/static"):
        return None

    if not check_rate_limit(ip):
        return jsonify({"error": "Too many requests. Please wait."}), 429

@app.route("/health")
def health():
    return jsonify({"gateway": "running", "time": time.strftime("%H:%M:%S")})


@app.route("/api/auth/login", methods=["POST"])
def login():
    """
    Called when user clicks LOGIN in the popup.
    Forwards to auth_service.py → /login
    """
    data = request.get_json()
    try:
        resp = requests.post(f"{SERVICES['auth']}/login", json=data, timeout=5)
        result = resp.json()


        if resp.status_code == 200 and "token" in result:
            active_tokens[result["token"]] = result.get("username", data.get("username"))

        return jsonify(result), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Auth service is offline. Start auth_service.py"}), 503

@app.route("/api/auth/register", methods=["POST"])
def register():
    """
    Called when user clicks SIGN UP in page2.html.
    Forwards to auth_service.py → /register
    """
    data = request.get_json()
    try:
        resp = requests.post(f"{SERVICES['auth']}/register", json=data, timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Auth service is offline. Start auth_service.py"}), 503

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """Logout — removes token."""
    data = request.get_json()
    token = data.get("token", "")
    if token in active_tokens:
        del active_tokens[token]
    try:
        resp = requests.post(f"{SERVICES['auth']}/logout", json=data, timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"message": "Logged out (auth service offline)"}), 200



@app.route("/api/user/profile", methods=["GET"])
def get_all_profiles():
    try:
        resp = requests.get(f"{SERVICES['user']}/profile", timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "User service is offline. Start user_service.py"}), 503

@app.route("/api/user/profile/<username>", methods=["GET"])
def get_profile(username):
    try:
        resp = requests.get(f"{SERVICES['user']}/profile/{username}", timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "User service is offline"}), 503

@app.route("/api/user/profile/<username>", methods=["PUT"])
def update_profile(username):
    try:
        resp = requests.put(
            f"{SERVICES['user']}/profile/{username}",
            json=request.get_json(), timeout=5
        )
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "User service is offline"}), 503


@app.route("/api/notif/send", methods=["POST"])
def send_notification():
    try:
        resp = requests.post(f"{SERVICES['notif']}/notify", json=request.get_json(), timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Notification service is offline. Start notif_service.py"}), 503

@app.route("/api/notif/log", methods=["GET"])
def notif_log():
    try:
        resp = requests.get(f"{SERVICES['notif']}/log", timeout=5)
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Notification service is offline"}), 503


if __name__ == "__main__":
    print("=" * 55)
    print("  CozMoz API Gateway — http://localhost:3000")
    print("=" * 55)
    print("  Services expected at:")
    print("    auth_service.py  → http://localhost:3000")
    print("    user_service.py  → http://localhost:3000")
    print("    notif_service.py → http://localhost:3000")
    print("=" * 55)
    app.run(debug=True, port=3000)