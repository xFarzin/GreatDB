"""Add imports table

Revision ID: 005_imports
Revises: 004_referrals
Create Date: 2024-05-10 12:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '005_imports'
down_revision: Union[str, None] = '004_referrals'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("""
    DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'importstatus') THEN
            CREATE TYPE importstatus AS ENUM ('QUEUED', 'RUNNING', 'PAUSED', 'COMPLETED', 'FAILED');
        END IF;
    END $$;
    """)
    import_status_enum = postgresql.ENUM('QUEUED', 'RUNNING', 'PAUSED', 'COMPLETED', 'FAILED', name='importstatus', create_type=False)

    op.create_table('import_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dataset_id', sa.Integer(), nullable=False),
    sa.Column('target_version', sa.Integer(), nullable=False),
    sa.Column('file_path', sa.String(), nullable=False),
    sa.Column('status', import_status_enum, nullable=False),
    sa.Column('total_bytes', sa.BigInteger(), nullable=True, server_default='0'),
    sa.Column('bytes_processed', sa.BigInteger(), nullable=True, server_default='0'),
    sa.Column('total_records', sa.BigInteger(), nullable=True, server_default='0'),
    sa.Column('records_processed', sa.BigInteger(), nullable=True, server_default='0'),
    sa.Column('current_stage', sa.String(), nullable=True, server_default='QUEUED'),
    sa.Column('error_log', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_import_jobs_id'), 'import_jobs', ['id'], unique=False)

    op.create_table('import_checkpoints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('last_byte_offset', sa.BigInteger(), nullable=True, server_default='0'),
    sa.Column('last_record_count', sa.BigInteger(), nullable=True, server_default='0'),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['import_jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_import_checkpoints_id'), 'import_checkpoints', ['id'], unique=False)
    op.create_index(op.f('ix_import_checkpoints_job_id'), 'import_checkpoints', ['job_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_import_checkpoints_job_id'), table_name='import_checkpoints', create_type=False)
    op.drop_index(op.f('ix_import_checkpoints_id'), table_name='import_checkpoints', create_type=False)
    op.drop_table('import_checkpoints')

    op.drop_index(op.f('ix_import_jobs_id'), table_name='import_jobs', create_type=False)
    op.drop_table('import_jobs')
