from app.models_old import Submission, StatusEnum
from app.storage import save_file

VALID_TRANSITIONS = {
    "pending": ["in_progress", "awaiting_payment"],
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

# ─── STRUCTURE DOMAIN ───────────────────────────────────────────

from app.models.structure import SuperCategory, Category, PDFItem

def create_super_category(db, name: str, order: int = 0):
    obj = SuperCategory(name=name, order=order)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def create_category(db, name: str, super_category_id, order: int = 0):
    obj = Category(name=name, super_category_id=super_category_id, order=order)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def create_pdf_item(db, title: str, file_url: str, category_id, description: str = None, order: int = 0):
    obj = PDFItem(title=title, file_url=file_url, category_id=category_id, description=description, order=order)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_full_structure(db):
    supers = db.query(SuperCategory).filter_by(is_active=True).order_by(SuperCategory.order).all()
    result = []
    for sc in supers:
        cats = []
        for cat in [c for c in sc.categories if c.is_active]:
            pdfs = [{"id": str(p.id), "title": p.title, "description": p.description, "file_url": p.file_url, "order": p.order}
                    for p in cat.pdf_items if p.is_active]
            cats.append({"id": str(cat.id), "name": cat.name, "order": cat.order, "pdfs": pdfs})
        result.append({"id": str(sc.id), "name": sc.name, "order": sc.order, "categories": cats})
    return result

def update_entity(db, model, entity_id, **kwargs):
    obj = db.query(model).filter_by(id=entity_id).first()
    if not obj:
        return None
    for k, v in kwargs.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def soft_delete(db, model, entity_id):
    obj = db.query(model).filter_by(id=entity_id).first()
    if obj:
        obj.is_active = False
        db.commit()
    return obj

def reorder_entities(db, model, items):
    for item in items:
        obj = db.query(model).filter_by(id=item["id"]).first()
        if obj:
            obj.order = item["order"]
    db.commit()
