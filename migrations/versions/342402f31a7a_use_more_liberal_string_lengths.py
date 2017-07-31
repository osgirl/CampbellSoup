"""Use more liberal string lengths

Revision ID: 342402f31a7a
Revises: 7d9d337d27c4
Create Date: 2017-07-31 15:17:23.419927

"""

# revision identifiers, used by Alembic.
revision = '342402f31a7a'
down_revision = '7d9d337d27c4'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column(
        'book',
        'edition',
        existing_type=sa.String(length=30),
        type_=sa.String(length=62),
        existing_nullable=True,
    )
    op.alter_column(
        'figure',
        'filename',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=False,
    )
    op.alter_column(
        'figure',
        'mimetype',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=False,
    )
    op.alter_column(
        'person',
        'email_address',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=True,
    )
    op.alter_column(
        'person',
        'full_name',
        existing_type=sa.String(length=60),
        type_=sa.String(length=254),
        existing_nullable=False,
    )
    op.alter_column(
        'person',
        'password_hash',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=True,
    )
    op.alter_column(
        'topic',
        'name',
        existing_type=sa.String(length=60),
        type_=sa.String(length=254),
        existing_nullable=False,
    )
    op.alter_column(
        'topic_book_binding',
        'chapter',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=True,
    )
    op.alter_column(
        'topic_book_binding',
        'figure',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=True,
    )
    op.alter_column(
        'topic_book_binding',
        'section',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=True,
    )
    op.alter_column(
        'topic_book_binding',
        'table',
        existing_type=sa.String(length=30),
        type_=sa.String(length=254),
        existing_nullable=True,
    )


def downgrade():
    op.alter_column(
        'topic_book_binding',
        'table',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        'topic_book_binding',
        'section',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        'topic_book_binding',
        'figure',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        'topic_book_binding',
        'chapter',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        'topic',
        'name',
        existing_type=sa.String(length=254),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        'person',
        'password_hash',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        'person',
        'full_name',
        existing_type=sa.String(length=254),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        'person',
        'email_address',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
    op.alter_column(
        'figure',
        'mimetype',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        'figure',
        'filename',
        existing_type=sa.String(length=254),
        type_=sa.String(length=30),
        existing_nullable=False,
    )
    op.alter_column(
        'book',
        'edition',
        existing_type=sa.String(length=62),
        type_=sa.String(length=30),
        existing_nullable=True,
    )
