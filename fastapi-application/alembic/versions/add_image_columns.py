"""add original_input column to images table

Revision ID: add_image_columns
Revises: c6e062161f53
Create Date: 2025-04-16 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'add_image_columns'
down_revision: Union[str, None] = 'c6e062161f53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Add original_input column to images table."""
    # Add original_input column
    op.add_column('images',
        sa.Column('original_input', sa.String(), nullable=True)
    )

def downgrade() -> None:
    """Remove original_input column from images table."""
    op.drop_column('images', 'original_input') 