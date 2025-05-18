from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY, password TEXT)''')
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'نام کاربری و رمز را وارد کنید'}), 400

    conn = get_db()
    cur = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({'message': 'نام کاربری موجود است'}), 400

    return jsonify({'message': 'ثبت نام با موفقیت انجام شد'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()

    if row and check_password_hash(row[0], password):
        return jsonify({'message': 'ورود موفق', 'username': username}), 200
    else:
        return jsonify({'message': 'نام کاربری یا رمز اشتباه است'}), 401

if __name__ == '__main__':
    app.run(debug=True)
