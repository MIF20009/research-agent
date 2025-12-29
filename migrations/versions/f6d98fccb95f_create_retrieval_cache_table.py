"""create retrieval_cache table

Revision ID: f6d98fccb95f
Revises: 70b6f1504b6d
Create Date: 2025-12-29 20:40:27.758966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6d98fccb95f'
down_revision: Union[str, Sequence[str], None] = '70b6f1504b6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "retrieval_cache",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("topic", sa.String(length=255), nullable=False, index=True),
        sa.Column("source", sa.String(length=50), nullable=False, server_default="openalex"),
        sa.Column("payload", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_retrieval_cache_topic_source", "retrieval_cache", ["topic", "source"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_retrieval_cache_topic_source", table_name="retrieval_cache")
    op.drop_table("retrieval_cache")
