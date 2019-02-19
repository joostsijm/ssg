"""page_add_parent

Revision ID: b87f52d28bb9
Revises: 476b167aef80
Create Date: 2019-02-19 22:38:47.415942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b87f52d28bb9'
down_revision = '476b167aef80'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('page', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'page', 'page', ['parent_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'page', type_='foreignkey')
    op.drop_column('page', 'parent_id')
