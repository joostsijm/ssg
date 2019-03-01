"""user_add_approved

Revision ID: d692d6e1a31d
Revises: 64c257f78218
Create Date: 2019-03-01 14:04:43.327766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd692d6e1a31d'
down_revision = '64c257f78218'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('approved', sa.Boolean(), server_default='f', nullable=True))


def downgrade():
    op.drop_column('user', 'approved')
