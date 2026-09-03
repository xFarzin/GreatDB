from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.core.db.base import Base

class ImportStatus(str, enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    target_version = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False) # MinIO path

    status = Column(Enum(ImportStatus), default=ImportStatus.QUEUED, nullable=False)

    # Progress tracking
    total_bytes = Column(BigInteger, default=0)
    bytes_processed = Column(BigInteger, default=0)
    total_records = Column(BigInteger, default=0)
    records_processed = Column(BigInteger, default=0)

    current_stage = Column(String, default="QUEUED")
    error_log = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    dataset = relationship("Dataset")

class ImportCheckpoint(Base):
    __tablename__ = "import_checkpoints"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("import_jobs.id"), nullable=False, unique=True)
    last_byte_offset = Column(BigInteger, default=0)
    last_record_count = Column(BigInteger, default=0)

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
