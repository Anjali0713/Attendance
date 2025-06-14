from flask import Blueprint, render_template, request, redirect, url_for, session

views = Blueprint('views', __name__)

# Simulated user database with roles
users = {
    "faculty": {"password": "pass123", "role": "faculty"},
    "student": {"password": "stud123", "role": "student"}
}
attendance_data = {}

@views.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user["password"] == password:
            session['username'] = username
            session['role'] = user["role"]
            return redirect(url_for('views.dashboard'))
    return render_template('login.html')

@views.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('views.login'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@views.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    if 'username' not in session or session.get('role') != 'faculty':
        return redirect(url_for('views.login'))
    if request.method == 'POST':
        student = request.form['student']
        attendance_data[student] = 'Present'
    return render_template('mark_attendance.html')

@views.route('/view_attendance')
def view_attendance():
    if 'username' not in session:
        return redirect(url_for('views.login'))
    if session.get('role') == 'student':
        username = session['username']
        filtered = {username: attendance_data.get(username, 'Absent')}
        return render_template('view_attendance.html', attendance=filtered)
    return render_template('view_attendance.html', attendance=attendance_data)
