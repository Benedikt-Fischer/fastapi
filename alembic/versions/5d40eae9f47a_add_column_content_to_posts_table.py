"""add column content to posts table

Revision ID: 5d40eae9f47a
Revises: 8b0e05ee45a4
Create Date: 2022-03-28 18:15:07.449988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d40eae9f47a'
down_revision = '8b0e05ee45a4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
