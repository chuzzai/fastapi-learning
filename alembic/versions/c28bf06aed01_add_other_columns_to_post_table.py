"""add other columns to post table

Revision ID: c28bf06aed01
Revises: 07f4a583ab3c
Create Date: 2026-10-03 16:22:45.702365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c28bf06aed01'
down_revision: Union[str, Sequence[str], None] = '07f4a583ab3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
