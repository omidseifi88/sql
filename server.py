from flask import Flask, request, jsonify
import json
import hashlib

app = Flask(__name__)

def load_users():
    try:
        with open("app/users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("app/users.json", "w") as f:
        json.dump(users, f)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400
    users = load_users()
    if username in users:
        return jsonify({"message": "User already exists."}), 400
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = hashed_password
    save_users(users)
    return jsonify({"message": "User registered successfully."}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Username and password are required."}), 400
    users = load_users()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if users.get(username) == hashed_password:
        return jsonify({"message": "Login successful."}), 200
    return jsonify({"message": "Invalid username or password."}), 400

if __name__ == "__main__":
    app.run(debug=True, port=2093)
