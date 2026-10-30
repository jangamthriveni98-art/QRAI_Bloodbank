from flask import Flask, render_template, request, redirect
import sqlite3, qrcode, os
from datetime import datetime, timedelta, date

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bloodbank.db')
    conn.execute('CREATE TABLE IF NOT EXISTS blood (id INTEGER PRIMARY KEY, blood_group TEXT, units INTEGER, joining_date TEXT, expiry_date TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS donors (id INTEGER PRIMARY KEY, name TEXT, blood_group TEXT, phone TEXT, location TEXT)')
    conn.close()

def auto_delete_expired():
    today = date.today().isoformat()
    conn = sqlite3.connect('bloodbank.db')
    # Expiry aypoyina blood ni auto delete
    conn.execute("DELETE FROM blood WHERE expiry_date < ?", (today,))
    conn.commit()
    conn.close()

def make_qr(bg):
    conn = sqlite3.connect('bloodbank.db')
    rows = conn.execute('SELECT units, joining_date, expiry_date FROM blood WHERE blood_group=?', (bg,)).fetchall()
    conn.close()
    if not rows: return
    total = sum(r[0] for r in rows)
    text = f"Blood Group: {bg}\nTotal Units: {total}\n"
    for u,j,e in rows:
        text += f"{u} Units | Join: {j} | Expiry: {e}\n"
    os.makedirs('static/qrs', exist_ok=True)
    qrcode.make(text).save(f'static/qrs/{bg}.png')

@app.route('/')
def home():
    init_db()
    auto_delete_expired()
    conn = sqlite3.connect('bloodbank.db')
    # Oke group ki oke row, units anni kaluputundi
    data = conn.execute('SELECT blood_group, SUM(units), MAX(expiry_date) FROM blood GROUP BY blood_group').fetchall()
    conn.close()
    for bg,_,_ in data:
        make_qr(bg)
    return render_template('index.html', data=data)

@app.route('/add_blood', methods=['GET','POST'])
def add_blood():
    if request.method == 'POST':
        jd = request.form['joining_date']
        exp = (datetime.strptime(jd, '%Y-%m-%d') + timedelta(days=35)).strftime('%Y-%m-%d')
        conn = sqlite3.connect('bloodbank.db')
        conn.execute('INSERT INTO blood (blood_group, units, joining_date, expiry_date) VALUES (?,?,?,?)',
                     (request.form['blood_group'], request.form['units'], jd, exp))
        conn.commit(); conn.close()
        return redirect('/')
    return render_template('add_blood.html')

@app.route('/add_donor', methods=['GET','POST'])
def add_donor():
    init_db()
    if request.method == 'POST':
        conn = sqlite3.connect('bloodbank.db')
        conn.execute('INSERT INTO donors (name, blood_group, phone, location) VALUES (?,?,?,?)',
                     (request.form['name'], request.form['blood_group'], request.form['phone'], request.form['location']))
        conn.commit(); conn.close()
        return redirect('/search_donor')
    return render_template('add_donor.html')

@app.route('/search_donor')
def search_donor():
    init_db()
    bg = request.args.get('blood_group')
    conn = sqlite3.connect('bloodbank.db')
    donors = conn.execute('SELECT * FROM donors WHERE blood_group=?', (bg,)).fetchall() if bg else conn.execute('SELECT * FROM donors').fetchall()
    conn.close()
    return render_template('search_donor.html', donors=donors)

if __name__ == '__main__':
    app.run(debug=True)