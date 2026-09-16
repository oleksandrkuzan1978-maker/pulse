"""Добавить категории и обязательную связь вопросов с категориями.


Revision ID: e5fb1b66a99f
Revises: ed89d0988d09
Create Date: 2026-09-16 15:13:37.546420
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5fb1b66a99f'
down_revision = 'ed89d0988d09'
branch_labels = None
depends_on = None


def upgrade():

    """Создать categories и добавить обязательный category_id без заполнения старых строк."""
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('questions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_questions_category_id', 'categories', ['category_id'], ['id'])


def downgrade():

    """Удалить связь вопросов с категориями и таблицу categories."""
    with op.batch_alter_table('questions', schema=None) as batch_op:

        batch_op.drop_constraint('fk_questions_category_id', type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('categories')

