""" Move all auth details into a dedicated Account model.

Revision ID: 2014baf2274c
Revises: 342402f31a7a
Create Date: 2018-01-12 14:47:33.853918

"""

# revision identifiers, used by Alembic.
revision = '2014baf2274c'
down_revision = '342402f31a7a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('account',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email_address', sa.String(length=254), nullable=True),
        sa.Column('password_hash', sa.String(length=128), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.Column('person_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['person_id'], ['person.id']),
        sa.ForeignKeyConstraint(['role_id'], ['user_role.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email_address'),
        sa.UniqueConstraint('person_id'),
    )
    op.drop_constraint('person_role_id_fkey', 'person', type_='foreignkey')
    # Destructive migration. These fields have not been used by the application
    # yet, so there should be no issue. Otherwise, manual account repair should
    # suffice.
    op.drop_column('person', 'role_id')
    op.drop_column('person', 'email_address')
    op.drop_column('person', 'password_hash')


def downgrade():
    op.add_column('person', sa.Column(
        'password_hash',
        sa.VARCHAR(length=254),
        autoincrement=False,
        nullable=True,
    ))
    op.add_column('person', sa.Column(
        'email_address',
        sa.VARCHAR(length=254),
        autoincrement=False,
        nullable=True,
    ))
    op.add_column('person', sa.Column(
        'role_id',
        sa.INTEGER(),
        autoincrement=False,
        nullable=True,
    ))
    op.create_foreign_key(
        'person_role_id_fkey',
        'person',
        'user_role',
        ['role_id'],
        ['id'],
    )
    op.drop_table('account')
