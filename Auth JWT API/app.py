import datetime
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)

app.config["FLASK_SECRET_KEY"] = secrets.token_hex(32)
app.config["JWT_SECRET_KEY"] = secrets.token_hex(32)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)

jwt = JWTManager(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your password",
    "database": "users_db",
}


def get_db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
    return conn


def initialize_database():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        print(f"Database '{db_config['database']}' ensured.")

        cursor.execute(f"USE {db_config['database']}")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(80) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """
        )
        conn.commit()
        print("Table 'users' ensured in the database.")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


initialize_database()


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    conn = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"msg": "User with this username already exists"}), 409

        hashed_password = generate_password_hash(password, method="scrypt")

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password),
        )
        conn.commit()
        return jsonify({"msg": "User created successfully"}), 201
    except Error as e:
        conn.rollback()
        print(f"Error during signup: {e}")
        return jsonify({"msg": f"Error creating user: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Missing username or password"}), 400

    username = data["username"]
    password = data["password"]

    conn = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, password FROM users WHERE username = %s", (username,)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            access_token = create_access_token(identity=str(user["id"]))
            return (
                jsonify({"msg": "Login successful", "access_token": access_token}),
                200,
            )
        else:
            return jsonify({"msg": "Invalid credentials"}), 401
    except Error as e:
        print(f"Error during login: {e}")
        return jsonify({"msg": f"Error during login: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/current-user", methods=["GET"])
@jwt_required()
def current_user():
    current_user_id = int(get_jwt_identity())

    conn = get_db_connection()
    if not conn:
        return jsonify({"msg": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username FROM users WHERE id = %s", (current_user_id,)
        )
        user = cursor.fetchone()
        if user:
            return (
                jsonify(
                    {
                        "user_id": user["id"],
                        "username": user["username"],
                        "msg": "Current user retrieved successfully",
                    }
                ),
                200,
            )
        return jsonify({"msg": "User not found"}), 404
    except Error as e:
        print(f"Error retrieving current user: {e}")
        return jsonify({"msg": f"Error retrieving current user: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
