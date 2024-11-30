from flask import Blueprint, request, jsonify
from database import get_db_connection
import bcrypt
from snowflake import SnowflakeGenerator
import sqlite3

auth_bp = Blueprint('auth', __name__)
generator = SnowflakeGenerator(69)

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user_id = next(generator)
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO users (id, username, password) VALUES (?, ?, ?)
        ''', (user_id, username, hashed_password))
        conn.commit()
        return jsonify({"message": f"User {username} registered successfully!", "user_id": user_id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        if conn:
            conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({"error": "Invalid username or password"}), 400

        stored_password = row[0]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 400
    finally:
        if conn:
            conn.close()