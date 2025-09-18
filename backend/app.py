from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sqlite3, os, time, csv, json
DB_PATH = os.path.join(os.path.dirname(__file__), 'attendance.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        roll INTEGER,
        class TEXT,
        guardian_phone TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        time TEXT,
        method TEXT
    )''')
    conn.commit()
    # load sample students if empty
    cur.execute('SELECT COUNT(*) as c FROM students')
    if cur.fetchone()['c'] == 0:
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'students.csv')
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cur.execute('INSERT INTO students (id,name,roll,class,guardian_phone) VALUES (?,?,?,?,?)',
                                (int(r['id']), r['name'], int(r['roll']), r['class'], r['guardian_phone']))
            conn.commit()
    conn.close()

app = Flask(__name__, static_folder='../static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('../static', 'teacher.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/students')
def api_students():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students ORDER BY roll')
    rows = [dict(x) for x in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/attendance', methods=['POST'])
def api_attendance():
    data = request.get_json()
    # data expected: {records: [{student_id, date, time, method}], origin: "teacher"}
    records = data.get('records', [])
    conn = get_db()
    cur = conn.cursor()
    inserted = 0
    for r in records:
        cur.execute('INSERT INTO attendance (student_id, date, time, method) VALUES (?,?,?,?)',
                    (r['student_id'], r['date'], r['time'], r.get('method','manual')))
        inserted += 1
        # mock notify parent (print to console)
        print(f"Notify guardian for student {r['student_id']}: mock SMS -> (would send to backend to integrate with SMS API)")
    conn.commit()
    conn.close()
    return jsonify({'status':'ok','inserted':inserted})

@app.route('/api/attendance/today')
def api_attendance_today():
    conn = get_db()
    cur = conn.cursor()
    today = time.strftime('%Y-%m-%d')
    cur.execute('''SELECT s.id as student_id, s.name, s.roll, 
                   (SELECT COUNT(*) FROM attendance a WHERE a.student_id=s.id AND a.date=?) as present
                   FROM students s ORDER BY s.roll''', (today,))
    rows = [dict(x) for x in cur.fetchall()]
    conn.close()
    return jsonify(rows)

@app.route('/api/attendance/all')
def api_attendance_all():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT a.id, a.student_id, s.name, a.date, a.time, a.method FROM attendance a JOIN students s ON s.id=a.student_id ORDER BY a.date DESC, a.time DESC LIMIT 200')
    rows = [dict(x) for x in cur.fetchall()]
    conn.close()
    return jsonify(rows)

# serve static files (teacher page)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../static', filename)

# Initialize DB on startup (works both locally and on Render)
init_db()

if __name__ == '__main__':
    print('Starting backend on http://0.0.0.0:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
