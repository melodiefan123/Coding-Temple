import time
import uuid
from typing import Dict, Any, List
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["reports"])

# In-memory data stores
reports_db: Dict[str, Dict[str, Any]] = {}
notification_log: List[Dict[str, str]] = []


# --- Pydantic Schemas ---
class CreateReportRequest(BaseModel):
    report_type: str
    rows: int = Field(default=10, ge=1)


class NotificationRequest(BaseModel):
    recipient: str
    message: str


# --- Background Task Functions ---
def generate_report(report_id: str, report_type: str, rows: int):
    if report_id in reports_db:
        reports_db[report_id]["status"] = "processing"

    # Simulate 2-second background work
    time.sleep(2)

    if report_id in reports_db:
        reports_db[report_id]["status"] = "complete"
        reports_db[report_id]["result"] = {
            "summary": f"Generated {report_type} report with {rows} rows."
        }


def send_notification(recipient: str, message: str):
    # Simulate work delay
    time.sleep(2)

    # Append to in-memory log
    notification_log.append({
        "recipient": recipient,
        "message": message,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })


# --- Endpoints ---
@router.post("", status_code=status.HTTP_202_ACCEPTED)
def create_report(
    payload: CreateReportRequest,
    background_tasks: BackgroundTasks
):
    report_id = str(uuid.uuid4())
    reports_db[report_id] = {
        "id": report_id,
        "status": "pending",
        "result": None
    }

    background_tasks.add_task(
        generate_report,
        report_id=report_id,
        report_type=payload.report_type,
        rows=payload.rows
    )

    return {"report_id": report_id, "status": "pending"}


@router.get("/{report_id}")
def get_report_status(report_id: str):
    if report_id not in reports_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    return reports_db[report_id]


@router.post("/notifications", status_code=status.HTTP_202_ACCEPTED)
def trigger_notification(
    payload: NotificationRequest,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        send_notification,
        recipient=payload.recipient,
        message=payload.message
    )
    return {"message": "Notification queued successfully."}


@router.get("/notifications/log")
def get_notifications_log():
    return {"logs": notification_log}