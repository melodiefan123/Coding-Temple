# app/utils/helpers.py
from datetime import datetime, timezone

def parse_date(value) -> datetime:
    """
    Safely converts a string or datetime object into a valid datetime instance.
    Returns datetime.utcnow() as a fallback if parsing fails or value is None.
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            # Handles ISO format strings like "2026-07-25T12:00:00Z" or "2026-07-25"
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
    return datetime.now(timezone.utc)