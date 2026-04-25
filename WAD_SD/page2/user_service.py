# ─────────────────────────────────────────────────────────────
# SERVICE LAYER — user_service.py
# Manages user profiles and preferences
# Run: python user_service.py   (runs on port 3002)
# ─────────────────────────────────────────────────────────────

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

profiles = {
    "admin": {"name": "Admin User", "email": "admin@cozmoz.com", "city": "Manila"},
}

@app.route("/health")
def health():
    return jsonify({"service": "user", "status": "ok"})

@app.route("/profile", methods=["GET"])
def get_all_profiles():
    return jsonify({"users": profiles})

@app.route("/profile/<username>", methods=["GET"])
def get_profile(username):
    user = profiles.get(username)
    if not user:
        return jsonify({"error": f"User '{username}' not found"}), 404
    return jsonify({"username": username, **user})

@app.route("/profile/<username>", methods=["PUT"])
def update_profile(username):
    if username not in profiles:
        return jsonify({"error": f"User '{username}' not found"}), 404
    profiles[username].update(request.get_json())
    return jsonify({"message": "Profile updated", "profile": profiles[username]})

@app.route("/profile/<username>", methods=["POST"])
def create_profile(username):
    """Called after registration to create a profile entry."""
    data = request.get_json()
    profiles[username] = {
        "name":  data.get("name", username),
        "email": data.get("email", ""),
        "city":  data.get("city", ""),
    }
    return jsonify({"message": f"Profile created for {username}"})

@app.route("/profile/<username>", methods=["DELETE"])
def delete_profile(username):
    if username not in profiles:
        return jsonify({"error": f"User '{username}' not found"}), 404
    del profiles[username]
    return jsonify({"message": f"User '{username}' deleted"})

if __name__ == "__main__":
    print("User Service running on http://localhost:3002")
    app.run(debug=True, port=3002)