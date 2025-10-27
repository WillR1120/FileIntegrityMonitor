from flask import Flask, render_template_string
import threading
from monitor import MONITORED_FOLDER, LOG_FOLDER, LOG_FILE, hash_file
import os
import time
from datetime import datetime

app = Flask(__name__)

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

file_hashes = {}
os.makedirs(LOG_FOLDER, exist_ok=True)

def monitor_files():
    while True:
        for filename in os.listdir(MONITORED_FOLDER):
            path = os.path.join(MONITORED_FOLDER, filename)
            if os.path.isfile(path):
                current_hash = hash_file(path)
                if filename not in file_hashes:
                    file_hashes[filename] = current_hash
                    with open(LOG_FILE, "a") as log:
                        log.write(f"{datetime.now()} - New file detected: {filename}\n")
                elif file_hashes[filename] != current_hash:
                    with open(LOG_FILE, "a") as log:
                        log.write(f"{datetime.now()} - File changed: {filename}\n")
                    file_hashes[filename] = current_hash
        time.sleep(5)

@app.route('/')
def home():
    lines = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for log in f.readlines()[-50:]:
                if " - " in log:
                    time_str, change = log.split(" - ", 1)
                    lines.append((time_str, change.strip()))
    return render_template_string(html_template, lines=lines)

if __name__ == "__main__":
    t = threading.Thread(target=monitor_files, daemon=True)
    t.start()
    app.run(debug=True)

