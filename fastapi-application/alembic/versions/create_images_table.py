"""create images table

Revision ID: create_images_table
Revises: 
Create Date: 2024-03-14

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'create_images_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('prompt', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('likes', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('images') 