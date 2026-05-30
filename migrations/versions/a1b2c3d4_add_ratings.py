"""add rating fields to staff and clients
Revision ID: a1b2c3d4e5f6
Revises: 03e2758c4c09
Create Date: 2026-05-30 12:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = '03e2758c4c09'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('rating_comment', sa.Text(), nullable=True))
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('rating_comment', sa.Text(), nullable=True))

def downgrade():
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.drop_column('rating_comment')
        batch_op.drop_column('rating')
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.drop_column('rating_comment')
        batch_op.drop_column('rating')
