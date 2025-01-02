from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
with open('secret_key.txt', 'r') as file:
    app.secret_key = file.read().strip()

# Separate lists for ongoing and completed tasks
ongoing_tasks = []
completed_tasks = []

# Simple user storage
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username not in users:
            hashed_password = generate_password_hash(password)
            users[username] = hashed_password
            session['user'] = username
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    user_authenticated = 'user' in session
    return render_template('index.html', ongoing_tasks=ongoing_tasks, completed_tasks=completed_tasks, user_authenticated=user_authenticated)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        ongoing_tasks.append(task)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    if 0 <= task_id < len(ongoing_tasks):
        completed_tasks.append(ongoing_tasks.pop(task_id))
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    if 0 <= task_id < len(ongoing_tasks):
        ongoing_tasks.pop(task_id)
    return redirect(url_for('index'))

@app.route('/delete_completed/<int:task_id>', methods=['POST'])
def delete_completed(task_id):
    if 0 <= task_id < len(completed_tasks):
        completed_tasks.pop(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
