from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Enum
from sqlalchemy.sql import func
import enum
from src.core.db.base import Base

class DatasetStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    QUEUED = "QUEUED"
    IMPORTING = "IMPORTING"
    INDEXING = "INDEXING"
    READY = "READY"
    DISABLED = "DISABLED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String(255), nullable=False)
    name_fa = Column(String(255), nullable=False)
    description_en = Column(String, nullable=True)
    description_fa = Column(String, nullable=True)

    status = Column(Enum(DatasetStatus), default=DatasetStatus.DRAFT, nullable=False)
    visible_to_users = Column(Boolean, default=False)
    searchable = Column(Boolean, default=False)

    record_count = Column(BigInteger, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
