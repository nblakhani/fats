"""make feedback visit_id nullable
Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-06-03
"""
from alembic import op
import sqlalchemy as sa

revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('visit_id', nullable=True)

def downgrade():
    with op.batch_alter_table('feedback', schema=None) as batch_op:
        batch_op.alter_column('visit_id', nullable=False)
