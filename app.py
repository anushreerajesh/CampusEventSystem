from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "campus_events.db"

# ------------------ Database Setup ------------------


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS colleges (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        college_id INTEGER,
                        FOREIGN KEY(college_id) REFERENCES colleges(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        event_type TEXT,
                        date TEXT,
                        college_id INTEGER,
                        FOREIGN KEY(college_id) REFERENCES colleges(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        event_id INTEGER,
                        UNIQUE(student_id, event_id),
                        FOREIGN KEY(student_id) REFERENCES students(id),
                        FOREIGN KEY(event_id) REFERENCES events(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        event_id INTEGER,
                        status TEXT,
                        UNIQUE(student_id, event_id),
                        FOREIGN KEY(student_id) REFERENCES students(id),
                        FOREIGN KEY(event_id) REFERENCES events(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        event_id INTEGER,
                        rating INTEGER,
                        comment TEXT,
                        FOREIGN KEY(student_id) REFERENCES students(id),
                        FOREIGN KEY(event_id) REFERENCES events(id))''')

    conn.commit()
    conn.close()


init_db()

# ------------------ APIs ------------------


@app.route("/events", methods=["POST", "GET"])
def events():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        cursor.execute(
            "INSERT INTO events (title, event_type, date, college_id) VALUES (?, ?, ?, ?)",
            (data["title"], data["event_type"],
             data["date"], data["college_id"])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Event created successfully!"})

    else:  # GET
        cursor.execute(
            "SELECT id, title, event_type, date, college_id FROM events")
        events = cursor.fetchall()
        conn.close()
        return jsonify([
            {"id": e[0], "title": e[1], "event_type": e[2],
                "date": e[3], "college_id": e[4]}
            for e in events
        ])


@app.route('/students', methods=['POST', 'GET'])
def students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        data = request.get_json()
        cursor.execute(
            "INSERT INTO students (name, email, college_id) VALUES (?, ?, ?)",
            (data["name"], data["email"], data["college_id"])
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Student added successfully!"})

    else:  # GET
        cursor.execute("SELECT id, name, email, college_id FROM students")
        students = cursor.fetchall()
        conn.close()
        return jsonify([
            {"id": s[0], "name": s[1], "email": s[2], "college_id": s[3]}
            for s in students
        ])


@app.route('/register', methods=['POST'])
def register_student():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO registrations (student_id, event_id) VALUES (?, ?)",
            (data['student_id'], data['event_id'])
        )
        conn.commit()
        msg = "Registration successful!"
    except sqlite3.IntegrityError:
        msg = "Student already registered!"
    conn.close()
    return jsonify({"message": msg})


@app.route('/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO attendance (student_id, event_id, status) VALUES (?, ?, ?)",
        (data['student_id'], data['event_id'], data['status'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Attendance marked!"})


@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (student_id, event_id, rating, comment) VALUES (?, ?, ?, ?)",
        (data['student_id'], data['event_id'],
         data['rating'], data.get('comment', ''))
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Feedback submitted!"})


@app.route('/reports/feedback/<int:event_id>', methods=['GET'])
def feedback_event(event_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT s.name, f.rating, f.comment FROM feedback f JOIN students s ON f.student_id=s.id WHERE f.event_id=?", (event_id,))
    data = cursor.fetchall()
    conn.close()
    return jsonify([{"student": d[0], "rating": d[1], "comment": d[2]} for d in data])

# ------------------ Reports ------------------


@app.route('/reports/registrations', methods=['GET'])
def registrations_report():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT e.title, COUNT(r.id) FROM events e LEFT JOIN registrations r ON e.id=r.event_id GROUP BY e.id ORDER BY COUNT(r.id) DESC"
    )
    data = cursor.fetchall()
    conn.close()
    return jsonify([{"title": d[0], "registrations": d[1]} for d in data])


@app.route('/reports/student_participation/<int:student_id>', methods=['GET'])
def student_participation(student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT e.title FROM events e JOIN attendance a ON e.id=a.event_id WHERE a.student_id=? AND a.status='present'",
        (student_id,)
    )
    data = cursor.fetchall()
    conn.close()
    return jsonify([d[0] for d in data])


@app.route('/reports/top_active_students', methods=['GET'])
def top_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT s.name, COUNT(a.id) as attended FROM students s "
        "JOIN attendance a ON s.id=a.student_id WHERE a.status='present' "
        "GROUP BY s.id ORDER BY attended DESC LIMIT 3"
    )
    data = cursor.fetchall()
    conn.close()
    return jsonify([{"name": d[0], "events_attended": d[1]} for d in data])


if __name__ == '__main__':
    app.run(debug=True)
