from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# HTML Template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>My To-Do List</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        input, button { padding: 8px; margin: 5px; }
        li { margin: 5px 0; }
        .done { text-decoration: line-through; color: gray; }
    </style>
</head>
<body>
    <h1>My To-Do List</h1>
    <form method="POST">
        <input name="task" placeholder="New task" required>
        <button>Add</button>
    </form>
    <ul>
        {% for i, task in enumerate(tasks) %}
        <li>
            <span class="{{ 'done' if task.done else '' }}">{{ task.text }}</span>
            <a href="/toggle/{{ i }}">Toggle</a>
            <a href="/delete/{{ i }}" style="color:red">Delete</a>
        </li>
        {% endfor %}
    </ul>
    <script>
        // Auto-save to localStorage
        const tasks = {{ tasks|tojson }};
        localStorage.setItem('tasks', JSON.stringify(tasks));
    </script>
</body>
</html>
"""

tasks = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global tasks
    if request.method == 'POST':
        tasks.append({"text": request.form['task'], "done": False})
    return render_template_string(TEMPLATE, tasks=tasks)

@app.route('/toggle/<int:i>')
def toggle(i):
    if 0 <= i < len(tasks):
        tasks[i]['done'] = not tasks[i]['done']
    return redirect(url_for('index'))

@app.route('/delete/<int:i>')
def delete(i):
    if 0 <= i < len(tasks):
        tasks.pop(i)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
