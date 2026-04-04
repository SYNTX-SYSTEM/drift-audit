from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid

class SuperCategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryResponse(BaseModel):
    id: uuid.UUID
    name: str
    super_category_id: uuid.UUID
    order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PDFItemResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    file_url: str
    category_id: uuid.UUID
    order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PDFItemPublic(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    file_url: str
    order: int

    class Config:
        from_attributes = True

class CategoryPublic(BaseModel):
    id: uuid.UUID
    name: str
    order: int
    pdfs: List[PDFItemPublic]

    class Config:
        from_attributes = True

class SuperCategoryPublic(BaseModel):
    id: uuid.UUID
    name: str
    order: int
    categories: List[CategoryPublic]

    class Config:
        from_attributes = True
