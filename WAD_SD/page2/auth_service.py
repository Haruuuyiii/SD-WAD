from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

# ── Points to your XAMPP/WAMP PHP API ─────────────────────────
PHP_API_BASE = "http://localhost/SD-WAD/WAD_SD/page2/api.php"

active_tokens = {}

def make_token(username):
    token = f"token-{username}-{int(time.time())}"
    active_tokens[token] = {"username": username, "created": time.time()}
    return token

def call_php(endpoint, data):
    """POST to api.php and return (json_dict, status_code)."""
    try:
        url = f"{PHP_API_BASE}/{endpoint}"
        resp = requests.post(url, json=data, timeout=5)
        return resp.json(), resp.status_code
    except requests.exceptions.RequestException as e:
        print(f"PHP API error: {e}")
        return {"error": "Database unreachable"}, 503

@app.route("/health")
def health():
    return jsonify({"service": "auth", "status": "ok"})

@app.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # ── Ask api.php to verify credentials against the real DB ──
    result, status = call_php("login", {"username": username, "password": password})

    if status == 200 and "token" in result:
        # Cache the token locally so gateway can verify it
        active_tokens[result["token"]] = {
            "username": result.get("username", username),
            "created":  time.time()
        }
        return jsonify(result), 200

    return jsonify({"error": result.get("error", "Invalid username or password")}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    result, status = call_php("register", data)
    return jsonify(result), status

@app.route("/verify", methods=["POST"])
def verify():
    data  = request.get_json()
    token = data.get("token", "")
    if token in active_tokens:
        return jsonify({"valid": True, "username": active_tokens[token]["username"]})
    return jsonify({"valid": False, "error": "Token not found or expired"}), 401

@app.route("/logout", methods=["POST"])
def logout():
    data  = request.get_json()
    token = data.get("token", "")
    if token in active_tokens:
        del active_tokens[token]
        return jsonify({"message": "Logged out successfully"})
    return jsonify({"error": "Token not found"}), 404

if __name__ == "__main__":
    print("Auth Service running on http://localhost:3001")
    app.run(debug=True, port=3001)