
from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# ── User "database" (replace with real DB/PHP in production)
USERS = {
    "admin": {"password": "1234",    "role": "admin"},
}

active_tokens = {}

def make_token(username):
    token = f"token-{username}-{int(time.time())}"
    active_tokens[token] = {"username": username, "created": time.time()}
    return token

@app.route("/health")
def health():
    return jsonify({"service": "auth", "status": "ok"})

@app.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    user = USERS.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    token = make_token(username)
    return jsonify({
        "message":  f"Welcome, {username}!",
        "token":    token,
        "username": username,
        "role":     user["role"]
    })

@app.route("/register", methods=["POST"])
def register():
    data     = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    if username in USERS:
        return jsonify({"error": "Username already exists"}), 409

    USERS[username] = {"password": password, "role": "user"}
    return jsonify({"message": f"Account created! Welcome, {username}!"})

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