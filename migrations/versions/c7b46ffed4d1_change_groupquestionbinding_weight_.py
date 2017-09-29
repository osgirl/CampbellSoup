"""Change GroupQuestionBinding.weight column to Float

Revision ID: c7b46ffed4d1
Revises: 410d73a04b1d
Create Date: 2017-04-10 17:06:05.529473

"""

# revision identifiers, used by Alembic.
revision = 'c7b46ffed4d1'
down_revision = '410d73a04b1d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'group_question_binding',
        'weight',
        existing_type=sa.INTEGER(),
        type_=sa.FLOAT(),
    )


def downgrade():
    op.alter_column(
        'group_question_binding',
        'weight',
        existing_type=sa.FLOAT(),
        type_=sa.INTEGER(),
    )
