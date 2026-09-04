"""add content column to posts table

Revision ID: 36f8f5feb210
Revises: 1bbd88b02e09
Create Date: 2026-09-04 21:05:30.428871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36f8f5feb210'
down_revision: Union[str, Sequence[str], None] = '1bbd88b02e09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
