"""Add subscriptions and payments

Revision ID: 003_subscriptions
Revises: 002_datasets_economy
Create Date: 2024-05-10 12:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_subscriptions'
down_revision: Union[str, None] = '002_datasets_economy'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('subscription_plans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('duration_days', sa.Integer(), nullable=False),
    sa.Column('price_stars', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscription_plans_id'), 'subscription_plans', ['id'], unique=False)

    op.create_table('user_subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True, server_default='true'),
    sa.ForeignKeyConstraint(['plan_id'], ['subscription_plans.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_subscriptions_id'), 'user_subscriptions', ['id'], unique=False)
    op.create_index(op.f('ix_user_subscriptions_user_id'), 'user_subscriptions', ['user_id'], unique=False)

    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('telegram_charge_id', sa.String(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('currency', sa.String(), nullable=True, server_default='XTR'),
    sa.Column('status', sa.String(), nullable=True, server_default='SUCCESS'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)
    op.create_index(op.f('ix_payments_telegram_charge_id'), 'payments', ['telegram_charge_id'], unique=True)
    op.create_index(op.f('ix_payments_user_id'), 'payments', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_payments_user_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_telegram_charge_id'), table_name='payments')
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')

    op.drop_index(op.f('ix_user_subscriptions_user_id'), table_name='user_subscriptions')
    op.drop_index(op.f('ix_user_subscriptions_id'), table_name='user_subscriptions')
    op.drop_table('user_subscriptions')

    op.drop_index(op.f('ix_subscription_plans_id'), table_name='subscription_plans')
    op.drop_table('subscription_plans')
