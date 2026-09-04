"""Add broadcasts

Revision ID: 007_broadcasts
Revises: 006_dataset_submissions
Create Date: 2024-05-10 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '007_broadcasts'
down_revision: Union[str, None] = '006_dataset_submissions'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'broadcaststatus') THEN
            CREATE TYPE broadcaststatus AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED');
        END IF;
    END $$;
    """)
    broadcast_status_enum = postgresql.ENUM('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', name='broadcaststatus', create_type=False)

    op.create_table('broadcasts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('message_en', sa.String(), nullable=True),
    sa.Column('message_fa', sa.String(), nullable=True),
    sa.Column('status', broadcast_status_enum, nullable=False),
    sa.Column('total_users', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('sent_count', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('failed_count', sa.Integer(), nullable=True, server_default='0'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_broadcasts_id'), 'broadcasts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_broadcasts_id'), table_name='broadcasts', create_type=False)
    op.drop_table('broadcasts')
