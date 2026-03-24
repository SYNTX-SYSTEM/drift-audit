from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from typing import Optional
from datetime import datetime

class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    awaiting_payment = "awaiting_payment"
    paid = "paid"
    delivered = "delivered"

class SubmissionResponse(BaseModel):
    id: UUID
    status: StatusEnum
    created_at: datetime
    model_config = {"from_attributes": True}

class SubmissionDetail(BaseModel):
    id: UUID
    url: str
    email: str
    language: Optional[str] = None
    status: StatusEnum
    payment_order_id: Optional[str] = None
    proton_link: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
