# utils/logging.py
from datetime import datetime
from collections import deque

class Logger:
    def __init__(self, max_lines=100):
        self.logs = deque(maxlen=max_lines)

    def log(self, message, category="INFO"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        formatted = f"{timestamp} 🔡️  {category.upper():<10} | {message}"
        print(formatted)
        self.logs.append(formatted)

    def __call__(self, message, category="INFO"):
        self.log(message, category)

    def tail(self, n=5):
        return list(self.logs)[-n:]

# Globale Instanz
log = Logger()
