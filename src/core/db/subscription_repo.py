from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from src.core.models.subscription import SubscriptionPlan, UserSubscription, Payment

class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_plans(self):
        result = await self.session.execute(select(SubscriptionPlan).where(SubscriptionPlan.is_active == True))
        return result.scalars().all()

    async def get_user_active_subscription(self, user_id: int) -> UserSubscription | None:
        now = datetime.now(timezone.utc)
        result = await self.session.execute(
            select(UserSubscription)
            .where(UserSubscription.user_id == user_id)
            .where(UserSubscription.is_active == True)
            .where(UserSubscription.end_date > now)
        )
        return result.scalars().first()

    async def record_payment(self, user_id: int, charge_id: str, amount: float, currency: str = "XTR") -> Payment | None:
        # Check idempotency
        existing = await self.session.execute(select(Payment).where(Payment.telegram_charge_id == charge_id))
        if existing.scalars().first():
            return None # Already processed

        payment = Payment(
            user_id=user_id,
            telegram_charge_id=charge_id,
            amount=amount,
            currency=currency
        )
        self.session.add(payment)
        await self.session.commit()
        await self.session.refresh(payment)
        return payment

    async def grant_subscription(self, user_id: int, plan_id: int) -> UserSubscription:
        plan = await self.session.get(SubscriptionPlan, plan_id)
        if not plan:
            raise ValueError("Invalid plan ID")

        now = datetime.now(timezone.utc)
        end_date = now + timedelta(days=plan.duration_days)

        # Extend if currently active?
        current_sub = await self.get_user_active_subscription(user_id)
        if current_sub:
            end_date = current_sub.end_date + timedelta(days=plan.duration_days)
            current_sub.end_date = end_date
            self.session.add(current_sub)
            await self.session.commit()
            return current_sub
        else:
            new_sub = UserSubscription(
                user_id=user_id,
                plan_id=plan.id,
                start_date=now,
                end_date=end_date,
                is_active=True
            )
            self.session.add(new_sub)
            await self.session.commit()
            await self.session.refresh(new_sub)
            return new_sub
