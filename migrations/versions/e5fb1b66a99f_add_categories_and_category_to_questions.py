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

    """Создать категории, заполнить старые вопросы и установить ограничения."""
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('questions') as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))

    connection = op.get_bind()
    categories = sa.table(
        'categories',
        sa.column('id', sa.Integer()),
        sa.column('name', sa.String()),
    )
    # Новая таблица пуста: создаём общую категорию для прежних вопросов.
    connection.execute(categories.insert().values(name='General'))
    category_id = connection.execute(sa.select(categories.c.id)).scalar_one()
    connection.execute(
        sa.text('UPDATE questions SET category_id = :id WHERE category_id IS NULL'),
        {'id': category_id},
    )

    with op.batch_alter_table('questions') as batch_op:
        batch_op.alter_column('category_id', existing_type=sa.Integer(), nullable=False)
        batch_op.create_foreign_key(
            'fk_questions_category_id', 'categories', ['category_id'], ['id']
        )


def downgrade():

    """Удалить связь вопросов с категориями и таблицу categories."""
    with op.batch_alter_table('questions', schema=None) as batch_op:

        batch_op.drop_constraint('fk_questions_category_id', type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('categories')

