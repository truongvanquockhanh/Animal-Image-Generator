"""gg modify

Revision ID: 1bdc14721c56
Revises: 816e485123cd
Create Date: 2025-04-18 14:52:56.619047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bdc14721c56'
down_revision: Union[str, None] = '816e485123cd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(), nullable=True))
    op.add_column('user', sa.Column('is_google_user', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'is_google_user')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
