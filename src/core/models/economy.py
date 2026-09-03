from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.core.db.base import Base

class TransactionType(str, enum.Enum):
    PURCHASE = "PURCHASE"
    SEARCH = "SEARCH"
    REFERRAL = "REFERRAL"
    REFERRAL_PURCHASE_BONUS = "REFERRAL_PURCHASE_BONUS"
    CONTRIBUTION_REWARD = "CONTRIBUTION_REWARD"
    MANUAL_ADJUSTMENT = "MANUAL_ADJUSTMENT"

class CreditTransaction(Base):
    """
    Append-only ledger for credits.
    Positive amount means addition, negative means deduction.
    """
    __tablename__ = "credit_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False) # Supporting fractional if needed, or Integer
    transaction_type = Column(Enum(TransactionType), nullable=False)
    reference_id = Column(String, nullable=True, index=True) # e.g. search_id, payment_id
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
