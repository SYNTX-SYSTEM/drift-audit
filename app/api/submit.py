from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services import create_submission
from app.schemas import SubmissionResponse
from app.email_service import send_pending_email, send_admin_alert

router = APIRouter()

@router.post("/submit", response_model=SubmissionResponse)
async def submit(
    background_tasks: BackgroundTasks,
    url: str = Form(...),
    email: str = Form(...),
    language: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    submission = create_submission(db, url, email, language, file)
    has_file = file.filename if file and file.filename else None

    background_tasks.add_task(send_pending_email, email, str(submission.id))
    background_tasks.add_task(send_admin_alert, str(submission.id), url, email, language, has_file)

    return submission
