# Optional helper to reset the demo DB and (optionally) generate QR codes for students.
# Usage: python init_db.py
import sqlite3, os, csv, qrcode, pathlib
HERE = pathlib.Path(__file__).parent
DB = HERE / 'attendance.db'
if DB.exists():
    DB.unlink()
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute('''CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, roll INTEGER, class TEXT, guardian_phone TEXT)''')
cur.execute('''CREATE TABLE attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER, date TEXT, time TEXT, method TEXT)''')
# load from students.csv
csv_path = HERE.parent / 'students.csv'
with open(csv_path) as f:
    reader = csv.DictReader(f)
    for r in reader:
        cur.execute('INSERT INTO students (id,name,roll,class,guardian_phone) VALUES (?,?,?,?,?)',
                    (int(r['id']), r['name'], int(r['roll']), r['class'], r['guardian_phone']))
conn.commit()
# generate QR codes (optional) to ../static/qr/
out = HERE.parent / 'static' / 'qr'
out.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute('SELECT id,name FROM students')
for sid, name in cur.fetchall():
    img = qrcode.make(str(sid))
    img.save(out / f'{sid}.png')
print('DB initialized, QR codes created in static/qr/ (if qrcode installed)')