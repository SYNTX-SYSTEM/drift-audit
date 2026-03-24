from app.models import Submission, StatusEnum
from app.storage import save_file

VALID_TRANSITIONS = {
    "pending": ["in_progress"],
    "in_progress": ["awaiting_payment"],
    "awaiting_payment": ["paid"],
    "paid": ["delivered"]
}

def create_submission(db, url, email, language, file):
    file_path = None
    if file:
        file_path = save_file(file)

    submission = Submission(
        url=url,
        email=email,
        language=language,
        file_path=file_path
    )

    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission

def transition_status(db, submission, new_status: str):
    current = submission.status.value
    allowed = VALID_TRANSITIONS.get(current, [])
    if new_status not in allowed:
        raise ValueError(f"Invalid transition: {current} -> {new_status}")
    submission.status = StatusEnum(new_status)
    db.commit()
    db.refresh(submission)
    return submission
