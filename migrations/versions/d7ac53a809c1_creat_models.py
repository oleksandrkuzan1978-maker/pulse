"""Сохранить совместимость с прежней дублирующей ревизией.

Revision ID: d7ac53a809c1
Revises: f7f26ce384b9
Таблицы создаются и удаляются только ревизией f7f26ce384b9.
"""

revision = "d7ac53a809c1"
down_revision = "f7f26ce384b9"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
