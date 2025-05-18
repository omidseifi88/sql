from flask import Flask, request, jsonify
import hashlib
import json
import os

app = Flask(__name__)
DATA_FILE = "users.json"

# تابع هش رمز عبور
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# بارگذاری داده‌های کاربر
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# ذخیره داده‌های کاربر
def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

# ثبت‌نام
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"status": "error", "message": "نام کاربری و رمز عبور الزامی است."}), 400

    users = load_users()
    if username in users:
        return jsonify({"status": "error", "message": "نام کاربری قبلاً ثبت شده."}), 409

    users[username] = hash_password(password)
    save_users(users)
    return jsonify({"status": "ok", "message": "ثبت‌نام با موفقیت انجام شد."})

# ورود
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    hashed = hash_password(password)
    if users.get(username) == hashed:
        return jsonify({"status": "ok", "message": "ورود موفق!"})
    else:
        return jsonify({"status": "error", "message": "نام کاربری یا رمز اشتباه است."}), 401

if __name__ == "__main__":
    app.run(debug=True)
