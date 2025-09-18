
Edu+ Aura -- Demo Package
=========================

What this demo contains:
- A Flask backend (backend/app.py) serving API endpoints and an admin dashboard.
- A lightweight teacher web app (static/teacher.html) that runs in any browser (phone or laptop).
- A sample students CSV and a helper script to generate QR codes for each student (optional).
- Offline-first behavior: the teacher page stores attendance locally and can sync to the backend.

How to run (Laptop):
1. Install Python 3.10+.
2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows powershell
3. Install requirements:
   pip install -r requirements.txt
4. Run the backend:
   cd backend
   python app.py
   By default the backend runs on http://0.0.0.0:5000

How to demo with your Pixel 6a:
1. Connect your laptop and phone to the same Wi‑Fi network.
2. On your phone open a browser and go to:
   http://<LAPTOP_LOCAL_IP>:5000/teacher.html
   (Replace <LAPTOP_LOCAL_IP> with your laptop IP on the Wi‑Fi network; e.g. 192.168.1.12)
3. Use the teacher page to mark attendance (Tap students or use "Simulate scan").
4. Click "Sync" on the teacher page to upload cached attendance to the backend.
5. Open the laptop browser at http://localhost:5000/dashboard to view the admin dashboard (live data).

Files summary:
- backend/app.py        # Flask backend + DB initialization
- backend/init_db.py    # optional helper to re-create sample DB and generate QR codes
- backend/templates/dashboard.html
- backend/static/*       # assets used by the dashboard
- static/teacher.html    # teacher web app (served by Flask static folder)
- students.csv           # sample students list
- README.md

Notes:
- Parent notifications are mocked in this demo. You can integrate SMS/WhatsApp APIs in backend/notify() easily.
- This demo uses simple authentication-free access for speed and demonstration; secure before production.

Good luck at SIH — show this flow in your presentation: Teacher (phone) -> Sync -> Dashboard (laptop) -> Parent alert (mock).
