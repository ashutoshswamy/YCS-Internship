from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your password",
    "database": "student_manager_db",
}


def initialize_database():
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        print(f"Database '{DB_CONFIG['database']}' ensured to exist.")

        cursor.execute(f"USE {DB_CONFIG['database']}")
        print(f"Using database '{DB_CONFIG['database']}'.")

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            grade VARCHAR(50) NOT NULL
        )
        """
        )

        conn.commit()
        print(
            "Table 'students' ensured to exist and database initialized successfully."
        )
    except Error as e:
        print(f"Error initializing database or table: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
        else:
            print("Failed to establish a database connection.")
            return None
    except Error as e:
        print("Failed to establish a database connection.")
        return None


initialize_database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/students", methods=["GET"])
def get_all_students():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, age, grade FROM students ORDER BY id DESC")
        students = cursor.fetchall()
        return jsonify(students)
    except Error as e:
        print(f"Error fetching students: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, age, grade FROM students WHERE id = %s", (student_id,)
        )
        student = cursor.fetchone()

        if student:
            return jsonify(student)
        else:
            return jsonify({"error": "Student not found"}), 404
    except Error as e:
        print(f"Error fetching student: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/students", methods=["POST"])
def create_student():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = None
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request must contain JSON data"}), 400
        if "name" not in data or not data["name"]:
            return jsonify({"error": "Student name is required"}), 400
        if "age" not in data or not isinstance(data["age"], int) or data["age"] <= 0:
            return jsonify({"error": "Student age must be a positive integer"}), 400
        if "grade" not in data or not data["grade"]:
            return jsonify({"error": "Student grade is required"}), 400

        name = data["name"]
        age = data["age"]
        grade = data["grade"]

        cursor = conn.cursor(dictionary=True)
        query = "INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, age, grade))
        conn.commit()

        new_student_id = cursor.lastrowid
        cursor.execute(
            "SELECT id, name, age, grade FROM students WHERE id = %s", (new_student_id,)
        )
        new_student = cursor.fetchone()

        return jsonify(new_student), 201
    except Error as e:
        print(f"Error creating student: {e}")
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = None
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must contain JSON data"}), 400

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM students WHERE id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404

        updates = []
        params = []

        if "name" in data and data["name"]:
            updates.append("name = %s")
            params.append(data["name"])
        if "age" in data and isinstance(data["age"], int) and data["age"] > 0:
            updates.append("age = %s")
            params.append(data["age"])
        if "grade" in data and data["grade"]:
            updates.append("grade = %s")
            params.append(data["grade"])

        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"
        params.append(student_id)

        cursor.execute(query, tuple(params))
        conn.commit()

        cursor.execute(
            "SELECT id, name, age, grade FROM students WHERE id = %s", (student_id,)
        )
        updated_student = cursor.fetchone()

        return jsonify(updated_student)
    except Error as e:
        print(f"Error updating student: {e}")
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = None
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM students WHERE id = %s", (student_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found"}), 404

        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        conn.commit()

        return (
            jsonify({"message": f"Student with ID {student_id} deleted successfully"}),
            200,
        )
    except Error as e:
        print(f"Error deleting student: {e}")
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
