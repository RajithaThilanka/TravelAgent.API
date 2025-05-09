from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class AuditMixin:
    """Mixin class for audit fields"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

class AuditLog(Base):
    """Model for tracking all changes in the system"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, nullable=False)
    record_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)  # CREATE, UPDATE, DELETE
    old_values = Column(String, nullable=True)  # JSON string of old values
    new_values = Column(String, nullable=True)  # JSON string of new values
    user_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True) 