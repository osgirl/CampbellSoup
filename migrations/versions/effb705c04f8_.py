"""empty message

Revision ID: effb705c04f8
Revises: None
Create Date: 2016-09-19 17:20:07.247048

"""

# revision identifiers, used by Alembic.
revision = 'effb705c04f8'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('author', sa.Text(), nullable=False),
        sa.Column('edition', sa.String(length=30), nullable=True),
        sa.Column('year', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('figure_kind',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('figure_tree',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('format',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('group_network',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question_kind',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('question_network',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question_status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('test',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('topic',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('user_role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('person',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('short_name', sa.String(length=30), nullable=False),
        sa.Column('full_name', sa.String(length=60), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('email_address', sa.String(length=30), nullable=True),
        sa.Column('password_hash', sa.String(length=30), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['user_role.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('short_name')
    )
    op.create_table('test_topic_binding',
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
        sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
        sa.PrimaryKeyConstraint('test_id', 'topic_id')
    )
    op.create_table('topic_book_binding',
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('chapter', sa.String(length=30), nullable=True),
        sa.Column('section', sa.String(length=30), nullable=True),
        sa.Column('figure', sa.String(length=30), nullable=True),
        sa.Column('table', sa.String(length=30), nullable=True),
        sa.Column('page', sa.String(length=30), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
        sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
        sa.PrimaryKeyConstraint('topic_id', 'book_id')
    )
    op.create_table('revision',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('commit_msg', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['person.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('figure',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('revision_id', sa.Integer(), nullable=False),
        sa.Column('kind_id', sa.Integer(), nullable=False),
        sa.Column('tree_id', sa.Integer(), nullable=False),
        sa.Column('ancestor_id', sa.Integer(), nullable=True),
        sa.Column('filename', sa.String(length=30), nullable=False),
        sa.Column('mimetype', sa.String(length=30), nullable=False),
        sa.Column('contents', sa.LargeBinary(), nullable=False),
        sa.ForeignKeyConstraint(['ancestor_id'], ['figure.id'], ),
        sa.ForeignKeyConstraint(['kind_id'], ['figure_kind.id'], ),
        sa.ForeignKeyConstraint(['revision_id'], ['revision.id'], ),
        sa.ForeignKeyConstraint(['tree_id'], ['figure_tree.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('revision_id', sa.Integer(), nullable=False),
        sa.Column('format_id', sa.Integer(), nullable=True),
        sa.Column('network_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['format_id'], ['format.id'], ),
        sa.ForeignKeyConstraint(['network_id'], ['group_network.id'], ),
        sa.ForeignKeyConstraint(['revision_id'], ['revision.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('introduction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('revision_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('source_code', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['revision_id'], ['revision.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('issue',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('raised_id', sa.Integer(), nullable=False),
        sa.Column('resolved_id', sa.Integer(), nullable=True),
        sa.Column('test_id', sa.Integer(), nullable=True),
        sa.Column('groupnet_id', sa.Integer(), nullable=True),
        sa.Column('questionnet_id', sa.Integer(), nullable=True),
        sa.Column('figuretree_id', sa.Integer(), nullable=True),
        sa.Column('assignee_id', sa.Integer(), nullable=True),
        sa.Column('deadline', sa.DateTime(), nullable=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['assignee_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['figuretree_id'], ['figure_tree.id'], ),
        sa.ForeignKeyConstraint(['groupnet_id'], ['group_network.id'], ),
        sa.ForeignKeyConstraint(['questionnet_id'], ['question_network.id'], ),
        sa.ForeignKeyConstraint(['raised_id'], ['revision.id'], ),
        sa.ForeignKeyConstraint(['resolved_id'], ['revision.id'], ),
        sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('revision_id', sa.Integer(), nullable=False),
        sa.Column('status_id', sa.Integer(), nullable=False),
        sa.Column('kind_id', sa.Integer(), nullable=True),
        sa.Column('network_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('bibliography', sa.Text(), nullable=True),
        sa.Column('difficulty', sa.Enum('low', 'average', 'high', name='difficulty'), nullable=True),
        sa.Column('quality', sa.Enum('low', 'average', 'high', name='quality'), nullable=True),
        sa.Column('source_code', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['kind_id'], ['question_kind.id'], ),
        sa.ForeignKeyConstraint(['network_id'], ['question_network.id'], ),
        sa.ForeignKeyConstraint(['revision_id'], ['revision.id'], ),
        sa.ForeignKeyConstraint(['status_id'], ['question_status.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_history',
        sa.Column('parent_id', sa.Integer(), nullable=False),
        sa.Column('child_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['child_id'], ['group.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['group.id'], ),
        sa.PrimaryKeyConstraint('parent_id', 'child_id')
    )
    op.create_table('group_introduction_binding',
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('intro_id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
        sa.ForeignKeyConstraint(['intro_id'], ['introduction.id'], ),
        sa.PrimaryKeyConstraint('group_id', 'intro_id')
    )
    op.create_table('group_question_binding',
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.PrimaryKeyConstraint('group_id', 'question_id')
    )
    op.create_table('introduction_figure_binding',
        sa.Column('intro_id', sa.Integer(), nullable=False),
        sa.Column('figure_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['figure_id'], ['figure.id'], ),
        sa.ForeignKeyConstraint(['intro_id'], ['introduction.id'], ),
        sa.PrimaryKeyConstraint('intro_id', 'figure_id')
    )
    op.create_table('issue_post',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('issue_id', sa.Integer(), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('revision_id', sa.Integer(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['person.id'], ),
        sa.ForeignKeyConstraint(['issue_id'], ['issue.id'], ),
        sa.ForeignKeyConstraint(['revision_id'], ['revision.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question_figure_binding',
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('figure_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['figure_id'], ['figure.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.PrimaryKeyConstraint('question_id', 'figure_id')
    )
    op.create_table('question_history',
        sa.Column('parent_id', sa.Integer(), nullable=False),
        sa.Column('child_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['child_id'], ['question.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['question.id'], ),
        sa.PrimaryKeyConstraint('parent_id', 'child_id')
    )
    op.create_table('question_topic_binding',
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('topic_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
        sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
        sa.PrimaryKeyConstraint('question_id', 'topic_id')
    )
    op.create_table('test_group_binding',
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
        sa.ForeignKeyConstraint(['test_id'], ['test.id'], ),
        sa.PrimaryKeyConstraint('test_id', 'group_id')
    )


def downgrade():
    op.drop_table('test_group_binding')
    op.drop_table('question_topic_binding')
    op.drop_table('question_history')
    op.drop_table('question_figure_binding')
    op.drop_table('issue_post')
    op.drop_table('introduction_figure_binding')
    op.drop_table('group_question_binding')
    op.drop_table('group_introduction_binding')
    op.drop_table('group_history')
    op.drop_table('question')
    op.drop_table('issue')
    op.drop_table('introduction')
    op.drop_table('group')
    op.drop_table('figure')
    op.drop_table('revision')
    op.drop_table('topic_book_binding')
    op.drop_table('test_topic_binding')
    op.drop_table('person')
    op.drop_table('user_role')
    op.drop_table('topic')
    op.drop_table('test')
    op.drop_table('question_status')
    op.drop_table('question_network')
    op.drop_table('question_kind')
    op.drop_table('group_network')
    op.drop_table('format')
    op.drop_table('figure_tree')
    op.drop_table('figure_kind')
    op.drop_table('book')
