
import os
import psycopg
from flask import Flask, request, jsonify, send_from_directory

# Create Flask application
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "frontend")
    if os.path.isdir(os.path.join(os.path.dirname(__file__), "frontend"))
    else os.path.join(os.path.dirname(__file__), "../frontend"),
    static_url_path=""
)

# PostgreSQL database connection
def get_db_connection():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", "5432")),
        dbname=os.environ.get("DB_NAME", "employee_db"),
        user=os.environ.get("DB_USER", "employee_admin"),
        password=os.environ["DB_PASSWORD"]
    )


# HOME API
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.static_folder, "index.html")


# GET API - Read all employees
@app.route("/employees", methods=["GET"])
def get_employees():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, department FROM employees ORDER BY id"
            )
            rows = cur.fetchall()

    employees = [
        {
            "id": row[0],
            "name": row[1],
            "department": row[2]
        }
        for row in rows
    ]

    return jsonify(employees), 200


# POST API - Create a new employee
@app.route("/employees", methods=["POST"])
def add_employee():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a JSON object"
        }), 400

    name = data.get("name")
    department = data.get("department")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "Employee name is required"
        }), 400

    if not isinstance(department, str) or not department.strip():
        return jsonify({
            "error": "Department is required"
        }), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employees (name, department)
                VALUES (%s, %s)
                RETURNING id, name, department
                """,
                (name.strip(), department.strip())
            )
            row = cur.fetchone()

    new_employee = {
        "id": row[0],
        "name": row[1],
        "department": row[2]
    }

    return jsonify(new_employee), 201


# PUT API - Update an existing employee
@app.route("/employees/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a JSON object"
        }), 400

    name = data.get("name")
    department = data.get("department")

    if not isinstance(name, str) or not name.strip():
        return jsonify({
            "error": "Employee name is required"
        }), 400

    if not isinstance(department, str) or not department.strip():
        return jsonify({
            "error": "Department is required"
        }), 400

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE employees
                SET name = %s, department = %s
                WHERE id = %s
                RETURNING id, name, department
                """,
                (name.strip(), department.strip(), employee_id)
            )
            row = cur.fetchone()

    if row is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    updated_employee = {
        "id": row[0],
        "name": row[1],
        "department": row[2]
    }

    return jsonify(updated_employee), 200


# DELETE API - Delete an employee
@app.route("/employees/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM employees
                WHERE id = %s
                RETURNING id
                """,
                (employee_id,)
            )
            row = cur.fetchone()

    if row is None:
        return jsonify({
            "error": "Employee not found"
        }), 404

    return jsonify({
        "message": "Employee deleted successfully",
        "id": row[0]
    }), 200


# Start Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)