from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'assessment_student_secret_key'

# Database connection helper
def get_db():
    db_file = app.config.get('DATABASE', 'students.db')
    conn = sqlite3.connect(db_file, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

# Create students table if not exists
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            course TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Student model with all required fields
class Student:
    def __init__(self, id, name, email, age, gender, course, password):
        self.id = id
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender
        self.course = course
        self.password = password

# Home page redirects to register or profile if already logged in
@app.route('/')
def home():
    if 'student_id' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('register'))

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        course = request.form.get('course', '').strip()
        password = request.form.get('password', '').strip()

        # Check required fields
        if not (name and email and age and gender and course and password):
            return render_template('register.html', error="All fields are required!"), 400

        try:
            age_int = int(age)
        except ValueError:
            return render_template('register.html', error="Age must be a valid number!"), 400

        if len(password) < 6:
            return render_template('register.html', error="Password must be at least 6 characters long!"), 400

        # Insert student into database using try/except
        conn = None
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (name, email, age, gender, course, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, age_int, gender, course, password))
            conn.commit()

            # Redirect to success page with registered name
            return redirect(url_for('success', name=name))

        except sqlite3.IntegrityError:
            return render_template('register.html', error="Email is already registered. Please login or use another email."), 400
        except sqlite3.Error as e:
            return render_template('register.html', error=f"Database error: {e}"), 500
        except Exception as e:
            return render_template('register.html', error=f"Something went wrong: {e}"), 500
        finally:
            if conn:
                conn.close()

    return render_template('register.html')

# Success page
@app.route('/success')
def success():
    name = request.args.get('name', 'Student')
    return render_template('success.html', name=name)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'student_id' in session:
        return redirect(url_for('profile'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            return render_template('login.html', error="Please enter email and password.")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()

        # Check credentials and create session
        if row and row['password'] == password:
            session['student_id'] = row['id']
            session['student_name'] = row['name']
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error="Invalid email or password.")

    return render_template('login.html')

# Profile page
@app.route('/profile')
def profile():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE id = ?', (session['student_id'],))
    row = cursor.fetchone()
    conn.close()

    if not row:
        session.clear()
        return redirect(url_for('login'))

    student = Student(
        id=row['id'],
        name=row['name'],
        email=row['email'],
        age=row['age'],
        gender=row['gender'],
        course=row['course'],
        password=row['password']
    )

    return render_template('profile.html', student=student)

# AJAX route to update course
@app.route('/update-course', methods=['POST'])
def update_course():
    if 'student_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    new_course = request.form.get('course')
    if not new_course:
        return jsonify({'success': False, 'message': 'No course selected'}), 400

    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE students SET course = ? WHERE id = ?', (new_course, session['student_id']))
        conn.commit()

        return jsonify({'success': True, 'course': new_course})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if conn:
            conn.close()

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
