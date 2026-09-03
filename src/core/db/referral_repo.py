from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.models.referral import Referral
from src.core.models.economy import TransactionType
from src.core.db.repository import EconomyRepository

class ReferralRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.economy_repo = EconomyRepository(session)

    async def register_referral(self, referrer_id: int, referred_id: int, join_reward: float = 2.0) -> bool:
        """
        Registers a referral and optionally grants a joining reward.
        Returns False if the referred user was already referred.
        """
        # Prevent self-referral
        if referrer_id == referred_id:
            return False

        existing = await self.session.execute(select(Referral).where(Referral.referred_user_id == referred_id))
        if existing.scalars().first():
            return False # Anti-abuse: User can only be referred once

        ref = Referral(referrer_id=referrer_id, referred_user_id=referred_id)
        self.session.add(ref)

        # Grant credits to the referrer
        if join_reward > 0:
            await self.economy_repo.add_transaction(
                user_id=referrer_id,
                amount=join_reward,
                tx_type=TransactionType.REFERRAL,
                reference_id=f"join_{referred_id}",
                description=f"Reward for referring user {referred_id}"
            )

        await self.session.commit()
        return True

    async def grant_purchase_bonus(self, referred_id: int, bonus_reward: float = 5.0) -> bool:
        """
        Called when a user makes a qualifying purchase. Grants bonus to their referrer.
        """
        ref_q = await self.session.execute(select(Referral).where(Referral.referred_user_id == referred_id))
        ref = ref_q.scalars().first()

        if not ref or ref.purchase_bonus_granted:
            return False

        ref.purchase_bonus_granted = True
        self.session.add(ref)

        if bonus_reward > 0:
            await self.economy_repo.add_transaction(
                user_id=ref.referrer_id,
                amount=bonus_reward,
                tx_type=TransactionType.REFERRAL_PURCHASE_BONUS,
                reference_id=f"purchase_bonus_{referred_id}",
                description=f"Purchase bonus from referred user {referred_id}"
            )

        await self.session.commit()
        return True
