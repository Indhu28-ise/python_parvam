from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import tempfile
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret123'
DB_PATH = Path(tempfile.gettempdir()) / "parvam_day2_database.db"

# ---------- DB CONNECTION ----------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ---------- CREATE TABLES ----------
def create_tables():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        course TEXT,
        phone TEXT)''')

    conn.commit()
    conn.close()

# ---------- AUTH ----------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",
                        (name, email, password))
            conn.commit()
            flash("Registered Successfully", "success")
            return redirect('/login')
        except:
            flash("Email already exists", "danger")

        conn.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/dashboard')
        else:
            flash("Invalid Credentials", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- DASHBOARD ----------

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

# ---------- CRUD ----------

@app.route('/students')
def students():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()

    return render_template('students.html', students=data)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        conn = get_db()
        cur = conn.cursor()

        cur.execute("INSERT INTO students(name,email,course,phone) VALUES(?,?,?,?)",
                    (request.form['name'],
                     request.form['email'],
                     request.form['course'],
                     request.form['phone']))
        conn.commit()
        conn.close()

        flash("Student Added", "success")
        return redirect('/students')

    return render_template('add_student.html')


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute("""UPDATE students SET 
                       name=?, email=?, course=?, phone=? 
                       WHERE id=?""",
                    (request.form['name'],
                     request.form['email'],
                     request.form['course'],
                     request.form['phone'],
                     id))
        conn.commit()
        conn.close()

        flash("Updated Successfully", "success")
        return redirect('/students')

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()

    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<int:id>')
def delete_student(id):
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("Deleted Successfully", "danger")
    return redirect('/students')


# ---------- RUN ----------
if __name__ == '__main__':
    create_tables()
    app.run(debug=False)
