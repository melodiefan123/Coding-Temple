import time
from datetime import datetime


def log_activity(user_id: int, action: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] User ID: {user_id} - Action: {action}\n"

    with open("activity_log.txt", "a") as f:
        f.write(log_entry)


def send_notification(email: str, message: str):
    # Simulate network delay (e.g., calling an external email API like SendGrid/Resend)
    time.sleep(2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Sent to {email}: {message}\n"

    with open("notification_log.txt", "a") as f:
        f.write(log_entry)