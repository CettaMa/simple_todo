from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Separate lists for ongoing and completed tasks
ongoing_tasks = []
completed_tasks = []

@app.route('/')
def index():
    return render_template('index.html', ongoing_tasks=ongoing_tasks, completed_tasks=completed_tasks)

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
    app.run(debug=True)
