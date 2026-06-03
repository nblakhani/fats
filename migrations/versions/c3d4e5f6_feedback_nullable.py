"""make feedback from_id nullable
Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-06-03
"""
from alembic import op
import sqlalchemy as sa

revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('from_id', nullable=True)

def downgrade():
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('from_id', nullable=False)
