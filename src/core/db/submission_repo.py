from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.core.models.dataset_submission import DatasetSubmission, SubmissionStatus
from src.core.models.economy import TransactionType
from src.core.db.repository import EconomyRepository

class SubmissionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.economy_repo = EconomyRepository(session)

    async def create_submission(self, user_id: int, name: str, description: str, file_path: str) -> DatasetSubmission:
        sub = DatasetSubmission(
            user_id=user_id,
            name=name,
            description=description,
            file_path=file_path,
            status=SubmissionStatus.QUARANTINED
        )
        self.session.add(sub)
        await self.session.commit()
        await self.session.refresh(sub)
        return sub

    async def review_submission(
        self,
        submission_id: int,
        reviewer_id: int,
        status: SubmissionStatus,
        notes: str = None,
        reward_credits: float = 0.0
    ) -> DatasetSubmission:
        sub = await self.session.get(DatasetSubmission, submission_id)
        if not sub:
            raise ValueError("Submission not found")

        sub.status = status
        sub.admin_reviewer_id = reviewer_id
        if notes:
            sub.review_notes = notes

        if status == SubmissionStatus.APPROVED and reward_credits > 0 and not sub.reward_granted:
            # Grant reward
            await self.economy_repo.add_transaction(
                user_id=sub.user_id,
                amount=reward_credits,
                tx_type=TransactionType.CONTRIBUTION_REWARD,
                reference_id=f"submission_{sub.id}",
                description=f"Reward for accepted dataset submission: {sub.name}"
            )
            sub.reward_granted = True

        self.session.add(sub)
        await self.session.commit()
        await self.session.refresh(sub)
        return sub
