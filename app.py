# CodeCraftHub - simple Flask API to track courses
import json, os
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)
FILE = "courses.json"
STATUSES = ["Not Started", "In Progress", "Completed"]
FIELDS = ["name", "description", "target_date", "status"]

# Read courses from the file (create the file if missing)
def load():
    if not os.path.exists(FILE):
        save([])
    with open(FILE) as f:
        return json.load(f)

# Save courses to the file
def save(courses):
    with open(FILE, "w") as f:
        json.dump(courses, f, indent=2)

# Check the data sent by the user, return an error message or None
def check(data, update=False):
    if not update:
        for field in FIELDS:
            if not data.get(field):
                return f"Missing required field: {field}"
    if "status" in data and data["status"] not in STATUSES:
        return "Invalid status. Use: Not Started, In Progress, Completed"
    if "target_date" in data:
        try:
            datetime.strptime(data["target_date"], "%Y-%m-%d")
        except Exception:
            return "target_date must be YYYY-MM-DD"
    return None

# File read/write errors
@app.errorhandler(OSError)
def file_error(e):
    return jsonify({"error": "File read/write error"}), 500

# POST - add a course
@app.route("/api/courses", methods=["POST"])
def add_course():
    data = request.get_json(silent=True) or {}
    error = check(data)
    if error:
        return jsonify({"error": error}), 400
    courses = load()
    course = {
        "id": max([c["id"] for c in courses], default=0) + 1,
        "name": data["name"],
        "description": data["description"],
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    courses.append(course)
    save(courses)
    return jsonify(course), 201

# GET - all courses
@app.route("/api/courses", methods=["GET"])
def get_courses():
    return jsonify(load())

# GET - statistics (optional challenge)
@app.route("/api/courses/stats", methods=["GET"])
def stats():
    courses = load()
    by_status = {s: sum(1 for c in courses if c["status"] == s) for s in STATUSES}
    return jsonify({"total_courses": len(courses), "by_status": by_status})

# GET - one course
@app.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):
    course = next((c for c in load() if c["id"] == id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course)

# PUT - update a course
@app.route("/api/courses/<int:id>", methods=["PUT"])
def update_course(id):
    data = request.get_json(silent=True) or {}
    courses = load()
    course = next((c for c in courses if c["id"] == id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    error = check(data, update=True)
    if error:
        return jsonify({"error": error}), 400
    for field in FIELDS:
        if field in data:
            course[field] = data[field]
    save(courses)
    return jsonify(course)

# DELETE - delete a course
@app.route("/api/courses/<int:id>", methods=["DELETE"])
def delete_course(id):
    courses = load()
    course = next((c for c in courses if c["id"] == id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    courses.remove(course)
    save(courses)
    return jsonify({"message": "Course deleted"})

if __name__ == "__main__":
    load()
    print("CodeCraftHub API is starting...")
    print("Data will be stored in:", os.path.abspath(FILE))
    print("API will be available at: http://localhost:5000")
    app.run(port=5000)
