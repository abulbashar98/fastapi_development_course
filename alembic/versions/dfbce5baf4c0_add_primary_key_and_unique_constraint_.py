"""add primary key and unique constraint to users table

Revision ID: dfbce5baf4c0
Revises: 31bf0f20642c
Create Date: 2026-09-05 10:56:02.358290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfbce5baf4c0'
down_revision: Union[str, Sequence[str], None] = '31bf0f20642c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_primary_key('users_pkey','users',['id'])
    op.create_unique_constraint('users_unique_constraint','users',['email'])
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('users_unique_constraint','users',type_='unique')
    op.drop_constraint('users_pkey','users',type_='primary')
    pass
