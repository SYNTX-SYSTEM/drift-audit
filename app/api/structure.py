from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import get_full_structure
from app.schemas_structure import SuperCategoryPublic
from typing import List

router = APIRouter()

@router.get("/structure", response_model=List[SuperCategoryPublic])
def get_structure(db: Session = Depends(get_db)):
    return get_full_structure(db)
