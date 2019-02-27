"""page_and_file_add_private_boolean

Revision ID: 64c257f78218
Revises: d4774c761a71
Create Date: 2019-02-26 21:09:02.780265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64c257f78218'
down_revision = 'd4774c761a71'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('file', sa.Column('private', sa.Boolean(), server_default='f', nullable=True))
    op.add_column('page', sa.Column('private', sa.Boolean(), server_default='f', nullable=True))


def downgrade():
    op.drop_column('page', 'private')
    op.drop_column('file', 'private')
