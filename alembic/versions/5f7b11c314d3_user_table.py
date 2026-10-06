"""user table

Revision ID: 5f7b11c314d3
Revises: f62f51d7cc27
Create Date: 2026-10-02 17:27:50.048669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f7b11c314d3'
down_revision: Union[str, Sequence[str], None] = 'f62f51d7cc27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.text('now()')),
        sa.UniqueConstraint('email', name='uq_users_email')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
