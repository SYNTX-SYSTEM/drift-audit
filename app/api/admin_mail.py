from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app.database import get_db
from app.api.admin import verify_admin
from app.models.structure import MailTemplate

router = APIRouter()

class TemplateUpdate(BaseModel):
    content: str

class TemplateResponse(BaseModel):
    id: str
    language: str
    key: str
    content: str

    class Config:
        from_attributes = True

@router.get("/admin/mail-templates")
def get_all_templates(db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    templates = db.query(MailTemplate).order_by(MailTemplate.language, MailTemplate.key).all()
    result = {}
    for t in templates:
        if t.language not in result:
            result[t.language] = {}
        result[t.language][t.key] = t.content
    return result

@router.get("/admin/mail-templates/{language}")
def get_templates_by_language(language: str, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    lang = language.upper()
    templates = db.query(MailTemplate).filter_by(language=lang).order_by(MailTemplate.key).all()
    if not templates:
        raise HTTPException(status_code=404, detail=f"No templates for language: {lang}")
    return {t.key: t.content for t in templates}

@router.put("/admin/mail-templates/{language}/{key}")
def update_template(language: str, key: str, body: TemplateUpdate, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    lang = language.upper()
    template = db.query(MailTemplate).filter_by(language=lang, key=key).first()
    if not template:
        raise HTTPException(status_code=404, detail=f"Template not found: {lang}/{key}")
    template.content = body.content
    db.commit()
    db.refresh(template)
    return {"language": template.language, "key": template.key, "content": template.content}

@router.post("/admin/mail-templates/{language}/{key}/reset")
def reset_template(language: str, key: str, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    from app.translations import TRANSLATIONS
    lang = language.upper()
    if lang not in TRANSLATIONS or key not in TRANSLATIONS[lang]:
        raise HTTPException(status_code=404, detail=f"No fallback for: {lang}/{key}")
    template = db.query(MailTemplate).filter_by(language=lang, key=key).first()
    if not template:
        raise HTTPException(status_code=404, detail=f"Template not found: {lang}/{key}")
    template.content = TRANSLATIONS[lang][key]
    db.commit()
    return {"status": "reset", "language": lang, "key": key}
