"""repair missing users table

Revision ID: a14c6e8b3f20
Revises: 5f7b11c314d3
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a14c6e8b3f20'
down_revision: Union[str, Sequence[str], None] = '5f7b11c314d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if not sa.inspect(op.get_bind()).has_table('users'):
        op.create_table(
            'users',
            sa.Column('id', sa.Integer, primary_key=True, nullable=False),
            sa.Column('email', sa.String, nullable=False, unique=True),
            sa.Column('password', sa.String, nullable=False),
            sa.Column(
                'created_at',
                sa.TIMESTAMP(timezone=True),
                nullable=False,
                server_default=sa.text('now()'),
            ),
        )


def downgrade() -> None:
    pass