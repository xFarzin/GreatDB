from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.core.db.base import Base

class SubmissionStatus(str, enum.Enum):
    QUARANTINED = "QUARANTINED"
    REVIEWING = "REVIEWING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class DatasetSubmission(Base):
    """
    User submitted dataset that sits in quarantine until admin review.
    """
    __tablename__ = "dataset_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    file_path = Column(String, nullable=False) # MinIO Quarantine bucket

    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.QUARANTINED, nullable=False)

    admin_reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    review_notes = Column(String, nullable=True)

    reward_granted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[admin_reviewer_id])
