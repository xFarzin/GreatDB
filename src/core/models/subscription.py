from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.db.base import Base

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration_days = Column(Integer, nullable=False)
    price_stars = Column(Integer, nullable=False) # Telegram Stars or fiat
    is_active = Column(Boolean, default=True)

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)

    user = relationship("User")
    plan = relationship("SubscriptionPlan")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    telegram_charge_id = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="XTR") # XTR is Telegram Stars
    status = Column(String, default="SUCCESS")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
