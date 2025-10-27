import os
import time
from hashlib import sha256

MONITORED_FOLDER = "monitored_files"
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "file_log.txt")

file_hashes = {}

def hash_file(path):
    h = sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def monitor_files():
    os.makedirs(LOG_FOLDER, exist_ok=True)
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

if __name__ == "__main__":
    monitor_files()
