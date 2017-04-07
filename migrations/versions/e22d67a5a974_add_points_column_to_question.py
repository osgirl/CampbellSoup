"""Add points column to Question

Revision ID: e22d67a5a974
Revises: 410d73a04b1d
Create Date: 2017-04-07 17:02:12.216497

"""

# revision identifiers, used by Alembic.
revision = 'e22d67a5a974'
down_revision = '410d73a04b1d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('question', sa.Column('points', sa.Float(), nullable=True))


def downgrade():
    op.drop_column('question', 'points')
