# ─────────────────────────────────────────────────────────────
# SERVICE LAYER — notif_service.py
# Sends email, SMS, and push notifications
# Run: python notif_service.py   (runs on port 3004)
# ─────────────────────────────────────────────────────────────

from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

notification_log = []

def send_email(to, subject, body):
    print(f"  [EMAIL] To: {to} | Subject: {subject}")
    return {"type": "email", "to": to, "subject": subject, "status": "sent"}

def send_sms(to, message):
    print(f"  [SMS] To: {to} | Message: {message}")
    return {"type": "sms", "to": to, "message": message, "status": "sent"}

def send_push(user_id, title, body):
    print(f"  [PUSH] User: {user_id} | Title: {title}")
    return {"type": "push", "user_id": user_id, "title": title, "status": "sent"}

@app.route("/health")
def health():
    return jsonify({"service": "notification", "status": "ok"})

@app.route("/notify", methods=["POST"])
def notify():
    data       = request.get_json()
    notif_type = data.get("type", "email")
    result     = {}

    if notif_type == "email":
        result = send_email(data.get("to", ""), data.get("subject", "Notification"), data.get("message", ""))
    elif notif_type == "sms":
        result = send_sms(data.get("to", ""), data.get("message", ""))
    elif notif_type == "push":
        result = send_push(data.get("user_id", ""), data.get("subject", "Notification"), data.get("message", ""))
    else:
        return jsonify({"error": f"Unknown type '{notif_type}'"}), 400

    result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    notification_log.append(result)
    return jsonify({"message": "Notification sent!", "result": result})

@app.route("/log", methods=["GET"])
def get_log():
    return jsonify({"total": len(notification_log), "notifications": notification_log})

if __name__ == "__main__":
    print("Notification Service running on http://localhost:3004")
    app.run(debug=True, port=3004)