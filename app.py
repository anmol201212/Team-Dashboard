from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Function to get the current week's dates
def get_current_week():
    today = datetime.today()
    start = today - timedelta(days=today.weekday())  # Monday
    dates = [(start + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)]  # Mon-Fri
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return zip(days, dates)

# Function to generate random colors
def generate_random_color():
    letters = '0123456789ABCDEF'
    color = ''.join(random.choice(letters) for _ in range(6))
    return color

@app.route('/')
def dashboard():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    # Generate a random color for each task
    task_colors = [generate_random_color() for _ in tasks]

    return render_template('dashboard.html', tasks=tasks, task_colors=task_colors)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form.get('name') or "NA"
        task = request.form.get('task') or "NA"
        wfo_days = ', '.join(request.form.getlist('wfo_days')) or "NA"
        leave_days = ', '.join(request.form.getlist('leave_days')) or "NA"

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (name, task, wfo_days, leave_days) VALUES (?, ?, ?, ?)", 
                  (name, task, wfo_days, leave_days))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    week_dates = get_current_week()
    return render_template('add_task.html', week_dates=week_dates)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name') or "NA"
        task = request.form.get('task') or "NA"
        wfo_days = ', '.join(request.form.getlist('wfo_days')) or "NA"
        leave_days = ', '.join(request.form.getlist('leave_days')) or "NA"
        
        c.execute("UPDATE tasks SET name = ?, task = ?, wfo_days = ?, leave_days = ? WHERE id = ?", 
                  (name, task, wfo_days, leave_days, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))

    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()

    week_dates = get_current_week()
    return render_template('edit_task.html', task=task, week_dates=week_dates)
