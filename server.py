from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "users.json"

def hash_password(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

@app.route("/register", methods=["POST"])
def register_api():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required."}), 400

    users = load_users()
    if username in users:
        return jsonify({"status": "error", "message": "Username already registered."}), 409

    users[username] = hash_password(password)
    save_users(users)
    return jsonify({"status": "ok", "message": "Registration was successful."})

@app.route("/login", methods=["POST"])
def login_api():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    users = load_users()
    if users.get(username) == hash_password(password):
        return jsonify({"status": "ok", "message": f"Welcome {username}"})
    else:
        return jsonify({"status": "error", "message": "The username or password is incorrect."}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 2093))
    app.run(host="0.0.0.0", port=port)