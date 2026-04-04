from fastapi import APIRouter, Depends, Header, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models_old import Submission, StatusEnum
from app.schemas import SubmissionDetail
from app.services import transition_status
from app.paypal_service import create_order
from app.email_service import send_ready_email
from app.config import settings

router = APIRouter()

def verify_admin(token: str = Header(...)):
    if token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router.get("/admin/submissions")
def list_submissions(
    status: Optional[StatusEnum] = None,
    db: Session = Depends(get_db),
    token: str = Depends(verify_admin)
):
    query = db.query(Submission)
    if status:
        query = query.filter(Submission.status == status)
    return query.order_by(Submission.created_at.desc()).all()

@router.patch("/admin/submissions/{submission_id}/ready")
async def mark_ready(
    submission_id: str,
    background_tasks: BackgroundTasks,
    proton_link: str,
    delivery_password: str,
    db: Session = Depends(get_db),
    token: str = Depends(verify_admin)
):
    submission = db.query(Submission).filter(
        Submission.id == submission_id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Not found")

    order_id, approve_link = create_order(str(submission.id), 49.00)

    submission.proton_link = proton_link
    submission.delivery_password = delivery_password
    submission.payment_order_id = order_id
    db.commit()

    transition_status(db, submission, "awaiting_payment")

    background_tasks.add_task(send_ready_email, submission.email, approve_link)

    return {"status": "awaiting_payment", "paypal_link": approve_link}

@router.patch("/admin/submissions/{submission_id}/status")
def update_status(
    submission_id: str,
    new_status: str,
    db: Session = Depends(get_db),
    token: str = Depends(verify_admin)
):
    submission = db.query(Submission).filter(
        Submission.id == submission_id
    ).first()

    if not submission:
        raise HTTPException(status_code=404, detail="Not found")

    transition_status(db, submission, new_status)
    return {"status": "updated", "new_status": new_status}
