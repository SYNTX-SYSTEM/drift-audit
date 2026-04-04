from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import get_full_structure

router = APIRouter()

@router.get("/structure")
def get_structure(db: Session = Depends(get_db)):
    return get_full_structure(db)
