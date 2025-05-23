"""update_image_likes_defau

Revision ID: c6e062161f53
Revises: 7882951ca0ce
Create Date: 2025-04-16 13:21:38.369362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c6e062161f53'
down_revision: Union[str, None] = '7882951ca0ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('prompt', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('likes', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='images_pkey')
    )
    # ### end Alembic commands ###
