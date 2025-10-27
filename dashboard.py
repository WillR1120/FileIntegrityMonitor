from flask import Flask, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = os.path.join("logs", "file_changes.log")

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>File Integrity Monitor Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; background: #111; color: #eee; text-align: center; }
        table { margin: 0 auto; border-collapse: collapse; width: 80%; }
        th, td { border: 1px solid #444; padding: 8px; }
        th { background: #333; }
        tr:nth-child(even) { background: #222; }
    </style>
</head>
<body>
    <h1>File Integrity Monitor Dashboard</h1>
    <p>Displaying the latest file changes in real time...</p>
    <table>
        <tr><th>Time</th><th>Change</th></tr>
        {% for line in lines %}
            <tr><td>{{ line[0] }}</td><td>{{ line[1] }}</td></tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def home():
    lines = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for log in f.readlines()[-50:]:
                if " - " in log:
                    time, change = log.split(" - ", 1)
                    lines.append((time, change.strip()))
    return render_template_string(html_template, lines=lines)

if __name__ == "__main__":
    app.run(debug=True)
