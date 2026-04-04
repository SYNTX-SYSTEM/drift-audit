from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from app.database import get_db
from app.api.admin import verify_admin
from app.models.structure import SuperCategory, Category, PDFItem
from app.services import (
    create_super_category, create_category, create_pdf_item,
    update_entity, soft_delete, reorder_entities
)
from app.storage import save_file

router = APIRouter()

class ReorderItem(BaseModel):
    id: str
    order: int

class ReorderPayload(BaseModel):
    type: str
    items: List[ReorderItem]

# ── SUPER CATEGORIES ──────────────────────────────────────────

@router.post("/admin/super-categories")
def create_sc(name: str, order: int = 0, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    return create_super_category(db, name, order)

@router.put("/admin/super-categories/{id}")
def update_sc(id: str, name: Optional[str] = None, order: Optional[int] = None, is_active: Optional[bool] = None,
              db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    kwargs = {k: v for k, v in {"name": name, "order": order, "is_active": is_active}.items() if v is not None}
    obj = update_entity(db, SuperCategory, id, **kwargs)
    if not obj:
        raise HTTPException(status_code=404)
    return obj

@router.delete("/admin/super-categories/{id}")
def delete_sc(id: str, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    soft_delete(db, SuperCategory, id)
    return {"status": "deleted"}

# ── CATEGORIES ────────────────────────────────────────────────

@router.post("/admin/categories")
def create_cat(name: str, super_category_id: str, order: int = 0,
               db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    return create_category(db, name, super_category_id, order)

@router.put("/admin/categories/{id}")
def update_cat(id: str, name: Optional[str] = None, order: Optional[int] = None, is_active: Optional[bool] = None,
               db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    kwargs = {k: v for k, v in {"name": name, "order": order, "is_active": is_active}.items() if v is not None}
    obj = update_entity(db, Category, id, **kwargs)
    if not obj:
        raise HTTPException(status_code=404)
    return obj

@router.delete("/admin/categories/{id}")
def delete_cat(id: str, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    soft_delete(db, Category, id)
    return {"status": "deleted"}

# ── PDF ITEMS ─────────────────────────────────────────────────

@router.post("/admin/pdfs")
async def create_pdf(
    title: str = Form(...),
    category_id: str = Form(...),
    description: Optional[str] = Form(None),
    order: int = Form(0),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(verify_admin)
):
    file_path = save_file(file)
    return create_pdf_item(db, title, file_path, category_id, description, order)

@router.put("/admin/pdfs/{id}")
def update_pdf(id: str, title: Optional[str] = None, description: Optional[str] = None,
               order: Optional[int] = None, is_active: Optional[bool] = None,
               db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    kwargs = {k: v for k, v in {"title": title, "description": description, "order": order, "is_active": is_active}.items() if v is not None}
    obj = update_entity(db, PDFItem, id, **kwargs)
    if not obj:
        raise HTTPException(status_code=404)
    return obj

@router.delete("/admin/pdfs/{id}")
def delete_pdf(id: str, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    soft_delete(db, PDFItem, id)
    return {"status": "deleted"}

# ── REORDER ───────────────────────────────────────────────────

@router.patch("/admin/reorder")
def reorder(payload: ReorderPayload, db: Session = Depends(get_db), token: str = Depends(verify_admin)):
    model_map = {
        "super_category": SuperCategory,
        "category": Category,
        "pdf": PDFItem
    }
    model = model_map.get(payload.type)
    if not model:
        raise HTTPException(status_code=400, detail="Invalid type")
    reorder_entities(db, model, [{"id": i.id, "order": i.order} for i in payload.items])
    return {"status": "reordered"}
