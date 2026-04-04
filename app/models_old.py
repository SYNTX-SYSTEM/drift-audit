import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base

class StatusEnum(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    awaiting_payment = "awaiting_payment"
    paid = "paid"
    delivered = "delivered"

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, nullable=False)
    email = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    language = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    payment_order_id = Column(String, nullable=True)
    proton_link = Column(String, nullable=True)
    delivery_password = Column(String, nullable=True)
    paypal_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaymentEvent(Base):
    __tablename__ = "payment_events"

    id = Column(String, primary_key=True)
    provider = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
