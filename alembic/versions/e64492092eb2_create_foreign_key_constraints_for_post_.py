"""create foreign key constraints for post table

Revision ID: e64492092eb2
Revises: dfbce5baf4c0
Create Date: 2026-09-05 11:25:21.919890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e64492092eb2'
down_revision: Union[str, Sequence[str], None] = 'dfbce5baf4c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('posts_fkey',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_fkey','posts')
    op.drop_column('posts','owner_id')
    pass
