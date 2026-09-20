"""Добавить общую категорию также в базы с уже применённой e5fb1b66a99f.

Revision ID: a31c9e7b4201
Revises: e5fb1b66a99f
"""

from alembic import op
import sqlalchemy as sa

revision = "a31c9e7b4201"
down_revision = "e5fb1b66a99f"
branch_labels = None
depends_on = None


def upgrade():
    """Создать категорию General, только если категории с таким именем ещё нет."""
    connection = op.get_bind()
    categories = sa.table(
        "categories",
        sa.column("id", sa.Integer()),
        sa.column("name", sa.String()),
    )
    existing = connection.execute(
        sa.select(categories.c.id).where(categories.c.name == "General").limit(1)
    ).first()
    if existing is None:
        connection.execute(categories.insert().values(name="General"))


def downgrade():
    # Категория могла существовать до миграции или уже использоваться вопросами.
    # Сохраняем пользовательские данные; схема в этой ревизии не менялась.
    """Сохранить категорию и пользовательские данные при откате отметки ревизии."""
    pass
