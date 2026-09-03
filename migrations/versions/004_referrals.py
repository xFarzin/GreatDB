"""Add referrals table

Revision ID: 004_referrals
Revises: 003_subscriptions
Create Date: 2024-05-10 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004_referrals'
down_revision: Union[str, None] = '003_subscriptions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('referrals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('referrer_id', sa.Integer(), nullable=False),
    sa.Column('referred_user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('purchase_bonus_granted', sa.Boolean(), nullable=True, server_default='false'),
    sa.ForeignKeyConstraint(['referred_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_referrals_id'), 'referrals', ['id'], unique=False)
    op.create_index(op.f('ix_referrals_referred_user_id'), 'referrals', ['referred_user_id'], unique=True)
    op.create_index(op.f('ix_referrals_referrer_id'), 'referrals', ['referrer_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_referrals_referrer_id'), table_name='referrals')
    op.drop_index(op.f('ix_referrals_referred_user_id'), table_name='referrals')
    op.drop_index(op.f('ix_referrals_id'), table_name='referrals')
    op.drop_table('referrals')
