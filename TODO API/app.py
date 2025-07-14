from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your password",
    "database": "todos_db",
}


def initialize_database():
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
        cursor.execute(f"USE {db_config['database']}")

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT FALSE
        )
        """
        )

        conn.commit()
        print("Database and table initialized successfully")
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


initialize_database()


@app.route("/")
def index():
    return render_template("index.html")


# API Routes
@app.route("/api/todos", methods=["GET"])
def get_todos():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM todos ORDER BY id DESC")
        todos = cursor.fetchall()

        for todo in todos:
            todo["completed"] = bool(todo["completed"])

        return jsonify(todos)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()

        if todo:
            todo["completed"] = bool(todo["completed"])
            return jsonify(todo)
        else:
            return jsonify({"error": "Todo not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/api/todos", methods=["POST"])
def create_todo():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()

        if not data or "title" not in data:
            return jsonify({"error": "Title is required"}), 400

        title = data["title"]
        description = data.get("description", "")
        completed = data.get("completed", False)

        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO todos (title, description, completed) VALUES (%s, %s, %s)",
            (title, description, completed),
        )
        conn.commit()

        todo_id = cursor.lastrowid
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        new_todo = cursor.fetchone()
        new_todo["completed"] = bool(new_todo["completed"])

        return jsonify(new_todo), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        data = request.get_json()

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cursor.fetchone()

        if not todo:
            return jsonify({"error": "Todo not found"}), 404

        updates = []
        params = []

        if "title" in data:
            updates.append("title = %s")
            params.append(data["title"])

        if "description" in data:
            updates.append("description = %s")
            params.append(data["description"])

        if "completed" in data:
            updates.append("completed = %s")
            params.append(data["completed"])

        if not updates:
            return jsonify({"error": "No fields to update"}), 400

        query = f"UPDATE todos SET {', '.join(updates)} WHERE id = %s"
        params.append(todo_id)

        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        updated_todo = cursor.fetchone()
        updated_todo["completed"] = bool(updated_todo["completed"])

        return jsonify(updated_todo)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM todos WHERE id = %s", (todo_id,))
        if not cursor.fetchone():
            return jsonify({"error": "Todo not found"}), 404

        cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        conn.commit()

        return jsonify({"message": "Todo deleted successfully"})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
