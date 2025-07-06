from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient, Doctor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # ✅ Important: allows column access by name
    c = conn.cursor()

    # Fetch patients and doctors from DB
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()

    c.execute("SELECT * FROM doctors")
    doctors = c.fetchall()

    conn.close()

    return render_template('index.html', patients=patients, doctors=doctors)

@app.route('/patients')
def patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

import sqlite3
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method=='POST':
         name = request.form['name']
         age = request.form['age']
         gender = request.form['gender']
         disease = request.form['disease']

         conn = sqlite3.connect('database.db')
         c = conn.cursor()
         c.execute("INSERT INTO patients (name, age, gender, disease) VALUES (?, ?, ?, ?)",
                  (name, age, gender, disease))
         conn.commit()
         conn.close()

         return redirect(url_for('index'))

    return render_template('add_patient.html')

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("DELETE FROM patients WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/edit_patient/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        disease = request.form['disease']

        c.execute("UPDATE patients SET name = ?, age = ?, gender = ?, disease = ? WHERE id = ?",
                  (name, age, gender, disease, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # GET request — show form with existing patient data
    c.execute("SELECT * FROM patients WHERE id = ?", (id,))
    patient = c.fetchone()
    conn.close()
    return render_template('edit_patient.html', patient=patient)

@app.route('/update_patient/<int:id>', methods=['POST'])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    patient.name = request.form['name']
    patient.age = request.form['age']
    patient.gender = request.form['gender']
    patient.disease = request.form['disease']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/doctors')
def doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

import sqlite3
@app.route('/add_doctor', methods=['GET', 'POST'])  # ✅ Accept both GET and POST
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO doctors (name, specialization, contact) VALUES (?, ?, ?)",
                  (name, specialization, contact))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('add_doctor.html')

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM doctors WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit_doctor/<int:id>', methods=['GET', 'POST'])
def edit_doctor(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']

        c.execute("UPDATE doctors SET name = ?, specialization = ?, contact = ? WHERE id = ?",
                  (name, specialization, contact, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    # GET request: fetch doctor data to edit
    c.execute("SELECT * FROM doctors WHERE id = ?", (id,))
    doctor = c.fetchone()
    conn.close()
    return render_template('edit_doctor.html', doctor=doctor)

if __name__ == '__main__':
    app.run(debug=True)