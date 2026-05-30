"""add LOB to visits and staff
Revision ID: 03e2758c4c09
Revises: f1eae2dff3d1
Create Date: 2026-05-30 05:16:04.763806
"""
from alembic import op
import sqlalchemy as sa

revision = '03e2758c4c09'
down_revision = 'f1eae2dff3d1'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lob', sa.String(length=200), nullable=True))
    with op.batch_alter_table('visits', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lob', sa.String(length=100), nullable=True))

def downgrade():
    with op.batch_alter_table('staff', schema=None) as batch_op:
        batch_op.drop_column('lob')
    with op.batch_alter_table('visits', schema=None) as batch_op:
        batch_op.drop_column('lob')