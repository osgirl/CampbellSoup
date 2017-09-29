"""Make introduction text nullable

Revision ID: 7d9d337d27c4
Revises: c7b46ffed4d1
Create Date: 2017-04-14 16:50:21.851276

"""

# revision identifiers, used by Alembic.
revision = '7d9d337d27c4'
down_revision = 'c7b46ffed4d1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'introduction',
        'text',
        existing_type=sa.TEXT(),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        'introduction',
        'text',
        existing_type=sa.TEXT(),
        nullable=False,
    )
