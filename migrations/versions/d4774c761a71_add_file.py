"""add_file

Revision ID: d4774c761a71
Revises: b87f52d28bb9
Create Date: 2019-02-23 18:33:44.647531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4774c761a71'
down_revision = 'b87f52d28bb9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=True),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('identifier', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('page_file',
    sa.Column('page_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
    sa.ForeignKeyConstraint(['page_id'], ['page.id'], ),
    sa.PrimaryKeyConstraint('page_id', 'file_id')
    )


def downgrade():
    op.drop_table('page_file')
    op.drop_table('file')
