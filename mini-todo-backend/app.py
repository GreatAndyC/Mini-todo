import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = Flask(__name__)
CORS(app)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute(
            """            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

@app.route("/health", methods=["GET"])
def health():
    return {"ok": True, "service": "todo-backend", "db_exists": os.path.exists(DB_PATH)}

@app.route("/tasks", methods=["GET"])
def list_tasks():
    with get_conn() as conn:
        rows = conn.execute("SELECT id, content, done, created_at FROM tasks ORDER BY id DESC").fetchall()
        tasks = [dict(id=row["id"], content=row["content"], done=bool(row["done"]), created_at=row["created_at"]) for row in rows]
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(force=True, silent=True) or {}
    content = (data.get("content") or "").strip()
    if not content:
        return jsonify({"error": "content is required"}), 400
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO tasks (content, done) VALUES (?, ?)", (content, 0))
        conn.commit()
        new_id = cur.lastrowid
        row = conn.execute("SELECT id, content, done, created_at FROM tasks WHERE id = ?", (new_id,)).fetchone()
    task = dict(id=row["id"], content=row["content"], done=bool(row["done"]), created_at=row["created_at"])
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return jsonify({"deleted": task_id})

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(force=True, silent=True) or {}
    fields = []
    values = []
    if "content" in data:
        fields.append("content = ?")
        values.append((data.get("content") or "").strip())
    if "done" in data:
        fields.append("done = ?")
        values.append(1 if data.get("done") else 0)
    if not fields:
        return jsonify({"error": "no fields to update"}), 400
    values.append(task_id)
    with get_conn() as conn:
        conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", values)
        conn.commit()
        row = conn.execute("SELECT id, content, done, created_at FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not row:
        return jsonify({"error": "not found"}), 404
    task = dict(id=row["id"], content=row["content"], done=bool(row["done"]), created_at=row["created_at"])
    return jsonify(task)

if __name__ == "__main__":
    # Ensure DB exists locally
    init_db()
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
