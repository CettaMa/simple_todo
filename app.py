from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import logging 
import coloredlogs
import re
import os

app = Flask(__name__)
csrf = CSRFProtect(app)

logger = logging.getLogger(__name__)
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)

formatter = coloredlogs.ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

coloredlogs.install(level='DEBUG')

# // Secure secret key
secret_key_path = os.path.join(os.path.dirname(__file__), 'config/secret_key.txt')
if os.path.exists(secret_key_path):
    with open(secret_key_path, 'r') as file:
        app.secret_key = file.read().strip()
else:
    logger.critical("Secret key file missing. Exiting.")
    raise FileNotFoundError("Secret key file not found!")

# // Separate lists for ongoing and completed tasks
ongoing_tasks = []
completed_tasks = []

# // Simple user storage
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # // Validate and sanitize input
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return render_template('register.html', error="Invalid username")
        if username not in users:
            hashed_password = generate_password_hash(password)
            users[username] = hashed_password
            session['user'] = username
            logger.info(f"Pengguna Baru terdaftar : '{username}'")
            return redirect(url_for('index'))
        else:
            logger.warning(f"Registrasi gagal: Pengguna '{username}' sudah terdaftar.")
            return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # // Validate and sanitize input
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return render_template('login.html', error="Invalid username")
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            logger.info(f"Pengguna melakukan login : '{username}'")
            return redirect(url_for('index'))
        else:
            logger.warning(f"Login gagal: Pengguna '{username}'.")
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    user = session.pop('user', None)
    if user:
        logger.info(f"Pengguna berhasil logout: '{user}'")
    else:
        logger.warning("Percobaan logout tanpa pengguna yang terautentikasi.")
    return redirect(url_for('login'))

@app.route('/')
def index():
    user_authenticated = 'user' in session
    if user_authenticated:
        logger.info(f"Pengguna terautentikasi mengakses halaman index. User: '{session['user']}'")
    else:
        logger.warning("Pengguna tidak terautentikasi mengakses halaman index.")
    return render_template('index.html', ongoing_tasks=ongoing_tasks, completed_tasks=completed_tasks, user_authenticated=user_authenticated)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    #  Validate and sanitize input
    if not re.match("^[a-zA-Z0-9_ ]+$", task):
        return "Invalid task", 400
    if task:
        ongoing_tasks.append(task)
        logger.info(f"Tugas baru ditambahkan dengan nama: '{task}'.")
    else:
        logger.warning("Percobaan penambahan tugas gagal")
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    if 0 <= task_id < len(ongoing_tasks):
        task = ongoing_tasks[task_id]
        completed_tasks.append(ongoing_tasks.pop(task_id))
        logger.info(f"Tugas diselesaikan: '{task}'")
    else:
        logger.warning(f"Tugas dengan ID '{task_id}' tidak valid untuk penyelesaian.")
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    if 0 <= task_id < len(ongoing_tasks):
        task = ongoing_tasks[task_id]
        ongoing_tasks.pop(task_id)
        logger.info(f"Tugas dihapus: '{task}'")
    else:
        logger.warning(f"Tugas dengan ID '{task_id}' tidak valid untuk penghapusan.")
    return redirect(url_for('index'))

@app.route('/delete_completed/<int:task_id>', methods=['POST'])
def delete_completed(task_id):
    if 0 <= task_id < len(completed_tasks):
        completed = completed_tasks[task_id]
        completed_tasks.pop(task_id)
        logger.info(f"Tugas selesai dihapus: '{completed}'")
    else:
        logger.warning(f"Tugas dengan ID '{task_id}' tidak valid untuk dihapus dari daftar selesai.")
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    logger.warning("404 error: Page not found")
    return "Page not found", 404

if __name__ == '__main__':
    app.run(debug=False)