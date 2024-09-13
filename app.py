# app.py

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                (id INTEGER PRIMARY KEY, 
                name TEXT, 
                task TEXT, 
                wfo_days TEXT, 
                upcoming_leave TEXT)''')
    conn.commit()
    conn.close()

# Route to show all tasks (Dashboard page)
@app.route('/')
def dashboard():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('dashboard.html', tasks=tasks)

# Route to show the form to add tasks (Form page)
@app.route('/add_task')
def add_task_page():
    return render_template('add_task.html')

@app.route('/save_task', methods=['POST'])
def save_task():
    name = request.form.get('name', 'NA')  # If no name is provided, default to 'NA'
    task = request.form.get('task', 'NA')  # If no task is provided, default to 'NA'
    
    # Collect multiple checkbox values for wfo_days or set to 'NA'
    wfo_days = ', '.join(request.form.getlist('wfo_days')) if request.form.getlist('wfo_days') else 'NA'
    
    upcoming_leave = request.form.get('upcoming_leave', 'NA')  # If no leave date is provided, default to 'NA'
    
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (name, task, wfo_days, upcoming_leave) VALUES (?, ?, ?, ?)", 
              (name, task, wfo_days, upcoming_leave))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))


@app.route('/edit_task/<int:task_id>')
def edit_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = c.fetchone()
    conn.close()

    if task:
        # task[4] now represents upcoming leave, so no need to split, just pass it directly
        return render_template('edit_task.html', task=task)
    else:
        return 'Task not found', 404

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    name = request.form.get('name', 'NA')
    task = request.form.get('task', 'NA')
    
    wfo_days = ', '.join(request.form.getlist('wfo_days')) if request.form.getlist('wfo_days') else 'NA'
    
    upcoming_leave = request.form.get('upcoming_leave', 'NA')
    
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET name = ?, task = ?, wfo_days = ?, upcoming_leave = ? WHERE id = ?", 
              (name, task, wfo_days, upcoming_leave, task_id))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
