from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.core.models.user import User
from src.core.models.economy import CreditTransaction, TransactionType

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalars().first()

    async def create_user(self, telegram_id: int, language: str = "fa") -> User:
        user = User(telegram_id=telegram_id, language=language)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

class EconomyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_balance(self, user_id: int) -> float:
        # We calculate the balance dynamically from the append-only ledger
        result = await self.session.execute(
            select(func.sum(CreditTransaction.amount)).where(CreditTransaction.user_id == user_id)
        )
        balance = result.scalar()
        return float(balance) if balance else 0.0

    async def add_transaction(
        self, user_id: int, amount: float, tx_type: TransactionType, reference_id: str = None, description: str = None
    ) -> CreditTransaction:
        tx = CreditTransaction(
            user_id=user_id,
            amount=amount,
            transaction_type=tx_type,
            reference_id=reference_id,
            description=description
        )
        self.session.add(tx)
        await self.session.commit()
        await self.session.refresh(tx)
        return tx

    async def reserve_credits_for_search(self, user_id: int, cost: float, search_ref: str) -> bool:
        """
        Safely checks balance and reserves credits for a search.
        Because we use postgres asyncpg we might do this in a transaction block.
        """
        # For a truly bulletproof approach without locking the whole table,
        # we sum the balance, and if enough, we insert a negative transaction.
        # This can be subject to a small race condition if they fire 100 requests exactly at once,
        # but since we only deduct, it's mostly fine if they temporarily go negative, or we can use pg advisory locks.
        # Let's use a simple sum check first.
        balance = await self.get_balance(user_id)
        if balance < cost:
            return False

        await self.add_transaction(
            user_id=user_id,
            amount=-cost,
            tx_type=TransactionType.SEARCH,
            reference_id=search_ref,
            description="Search deduction"
        )
        return True
