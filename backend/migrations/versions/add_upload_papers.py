"""add upload_papers field and run_papers table

Revision ID: add_upload_papers
Revises: f6d98fccb95f
Create Date: 2025-01-13 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_upload_papers'
down_revision: Union[str, Sequence[str], None] = 'f6d98fccb95f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add upload_papers field to runs table
    op.add_column('runs', sa.Column('upload_papers', sa.Boolean(), nullable=False, server_default='false'))
    
    # Create run_papers junction table
    op.create_table('run_papers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('paper_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['run_id'], ['runs.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_run_papers_id'), 'run_papers', ['id'], unique=False)
    op.create_index(op.f('ix_run_papers_run_id'), 'run_papers', ['run_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop run_papers table
    op.drop_index(op.f('ix_run_papers_run_id'), table_name='run_papers')
    op.drop_index(op.f('ix_run_papers_id'), table_name='run_papers')
    op.drop_table('run_papers')
    
    # Remove upload_papers field from runs table
    op.drop_column('runs', 'upload_papers')
