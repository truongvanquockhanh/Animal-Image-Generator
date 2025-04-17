"""update_image_likes_defa

Revision ID: 816e485123cd
Revises: add_image_columns
Create Date: 2025-04-16 15:31:05.648347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '816e485123cd'
down_revision: Union[str, None] = 'add_image_columns'
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
    sa.Column('is_suggested', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('original_input', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='images_pkey')
    )
    # ### end Alembic commands ###
