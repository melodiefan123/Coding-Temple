import time
from datetime import datetime
from pathlib import Path

# Base directory relative to this file: root of the repository
BASE_DIR = Path(__file__).resolve().parent.parent
ACTIVITY_LOG_PATH = BASE_DIR / "activity_log.txt"
NOTIFICATION_LOG_PATH = BASE_DIR / "notification_log.txt"


def log_activity(user_id: int, action: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User ID: {user_id} - Action: {action}\n"

    with open(ACTIVITY_LOG_PATH, "a") as f:
        f.write(log_entry)


def send_notification(email: str, message: str):
    # Simulate network delay (e.g., calling an external email API like SendGrid/Resend)
    time.sleep(2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Sent to {email}: {message}\n"

    with open(NOTIFICATION_LOG_PATH, "a") as f:
        f.write(log_entry)