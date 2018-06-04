"""empty message

Revision ID: 68bcb0d92f5a
Revises: 2014baf2274c
Create Date: 2018-06-04 15:02:19.597768

"""

# revision identifiers, used by Alembic.
revision = '68bcb0d92f5a'
down_revision = '2014baf2274c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('activation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=16), nullable=False),
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('expires', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token'),
    )


def downgrade():
    op.drop_table('activation')
