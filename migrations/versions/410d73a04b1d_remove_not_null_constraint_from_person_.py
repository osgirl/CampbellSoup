"""Remove not null constraint from Person.role_id

Revision ID: 410d73a04b1d
Revises: effb705c04f8
Create Date: 2017-04-04 17:57:38.195729

"""

# revision identifiers, used by Alembic.
revision = '410d73a04b1d'
down_revision = 'effb705c04f8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'person',
        'role_id',
        existing_type=sa.INTEGER(),
        nullable=True,
    )


def downgrade():
    op.alter_column(
        'person',
        'role_id',
        existing_type=sa.INTEGER(),
        nullable=False,
    )
