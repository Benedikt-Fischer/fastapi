"""add last few columns to posts table

Revision ID: b3bd57a9639f
Revises: 22b02b29dee6
Create Date: 2022-03-28 19:03:06.377892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3bd57a9639f'
down_revision = '22b02b29dee6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
