"""Add dataset submissions

Revision ID: 006_dataset_submissions
Revises: 005_imports
Create Date: 2024-05-10 12:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '006_dataset_submissions'
down_revision: Union[str, None] = '005_imports'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'submissionstatus') THEN
            CREATE TYPE submissionstatus AS ENUM ('QUARANTINED', 'REVIEWING', 'APPROVED', 'REJECTED');
        END IF;
    END $$;
    """)
    submission_status_enum = postgresql.ENUM('QUARANTINED', 'REVIEWING', 'APPROVED', 'REJECTED', name='submissionstatus', create_type=False)

    op.create_table('dataset_submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('status', submission_status_enum, nullable=False),
    sa.Column('admin_reviewer_id', sa.Integer(), nullable=True),
    sa.Column('review_notes', sa.String(), nullable=True),
    sa.Column('reward_granted', sa.Boolean(), nullable=True, server_default='false'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['admin_reviewer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dataset_submissions_id'), 'dataset_submissions', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_dataset_submissions_id'), table_name='dataset_submissions', create_type=False)
    op.drop_table('dataset_submissions')
