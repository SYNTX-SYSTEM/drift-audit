from fastapi import APIRouter, Request, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models_old import PaymentEvent, Submission, StatusEnum
from app.email_service import send_delivery_link, send_delivery_password

router = APIRouter()

@router.post("/payment/webhook")
async def paypal_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    payload = await request.json()
    event_id = payload.get("id")
    event_type = payload.get("event_type")

    if not event_id:
        raise HTTPException(status_code=400, detail="Missing event ID")

    existing = db.query(PaymentEvent).filter_by(id=event_id).first()
    if existing:
        return {"status": "already_processed"}

    payment_event = PaymentEvent(
        id=event_id,
        provider="paypal",
        event_type=event_type,
        payload=payload,
        processed=False
    )
    db.add(payment_event)
    db.commit()

    if event_type == "CHECKOUT.ORDER.APPROVED":
        resource = payload.get("resource", {})
        purchase_units = resource.get("purchase_units", [])

        if purchase_units:
            submission_id = purchase_units[0].get("custom_id")
            submission = db.query(Submission).filter(
                Submission.id == submission_id
            ).first()

            if submission:
                submission.status = StatusEnum.paid
                db.commit()

                background_tasks.add_task(send_delivery_link, submission.email, submission.proton_link)
                background_tasks.add_task(send_delivery_password, submission.email, submission.delivery_password)

    payment_event.processed = True
    db.commit()

    return {"status": "processed"}
