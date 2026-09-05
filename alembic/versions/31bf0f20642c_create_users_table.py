"""create users table

Revision ID: 31bf0f20642c
Revises: 36f8f5feb210
Create Date: 2026-09-05 10:29:46.916069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31bf0f20642c'
down_revision: Union[str, Sequence[str], None] = '36f8f5feb210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
