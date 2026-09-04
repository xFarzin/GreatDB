"""Add datasets and economy tables

Revision ID: 002_datasets_economy
Revises: 001_initial
Create Date: 2024-05-10 12:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '002_datasets_economy'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'datasetstatus') THEN
            CREATE TYPE datasetstatus AS ENUM ('DRAFT', 'QUEUED', 'IMPORTING', 'INDEXING', 'READY', 'DISABLED', 'FAILED', 'ARCHIVED');
        END IF;
    END $$;
    """)
    # datasets
    dataset_status_enum = postgresql.ENUM('DRAFT', 'QUEUED', 'IMPORTING', 'INDEXING', 'READY', 'DISABLED', 'FAILED', 'ARCHIVED', name='datasetstatus', create_type=False)

    op.create_table('datasets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_fa', sa.String(length=255), nullable=False),
    sa.Column('description_en', sa.String(), nullable=True),
    sa.Column('description_fa', sa.String(), nullable=True),
    sa.Column('status', dataset_status_enum, nullable=False),
    sa.Column('visible_to_users', sa.Boolean(), nullable=True),
    sa.Column('searchable', sa.Boolean(), nullable=True),
    sa.Column('record_count', sa.BigInteger(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_datasets_id'), 'datasets', ['id'], unique=False)

    # economy

    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'transactiontype') THEN
            CREATE TYPE transactiontype AS ENUM ('PURCHASE', 'SEARCH', 'REFERRAL', 'REFERRAL_PURCHASE_BONUS', 'CONTRIBUTION_REWARD', 'MANUAL_ADJUSTMENT');
        END IF;
    END $$;
    """)
    transaction_type_enum = postgresql.ENUM('PURCHASE', 'SEARCH', 'REFERRAL', 'REFERRAL_PURCHASE_BONUS', 'CONTRIBUTION_REWARD', 'MANUAL_ADJUSTMENT', name='transactiontype', create_type=False)

    op.create_table('credit_transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('transaction_type', transaction_type_enum, nullable=False),
    sa.Column('reference_id', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_credit_transactions_id'), 'credit_transactions', ['id'], unique=False)
    op.create_index(op.f('ix_credit_transactions_reference_id'), 'credit_transactions', ['reference_id'], unique=False)
    op.create_index(op.f('ix_credit_transactions_user_id'), 'credit_transactions', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_credit_transactions_user_id'), table_name='credit_transactions', create_type=False)
    op.drop_index(op.f('ix_credit_transactions_reference_id'), table_name='credit_transactions', create_type=False)
    op.drop_index(op.f('ix_credit_transactions_id'), table_name='credit_transactions', create_type=False)
    op.drop_table('credit_transactions')

    op.drop_index(op.f('ix_datasets_id'), table_name='datasets', create_type=False)
    op.drop_table('datasets')
