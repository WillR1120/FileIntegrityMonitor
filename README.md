# File Integrity Monitor

A Python project that monitors a folder for file changes and displays a live dashboard in your browser.

## Features

- Detects new files added to the monitored folder
- Tracks changes to existing files
- Maintains a log of all file changes
- Real-time web dashboard built with Flask
- Live updates every few seconds

## Tech Stack

- Python 3.11
- Flask
- hashlib (SHA-256 hashing)
- HTML/CSS for dashboard
- threading for background monitoring

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YourUsername/FileIntegrityMonitor.git
cd FileIntegrityMonitor
