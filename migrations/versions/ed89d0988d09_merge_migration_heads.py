"""Сохранить идентификатор прежнего слияния в линейной истории.

Revision ID: ed89d0988d09
Revises: d7ac53a809c1
Create Date: 2026-09-16 15:04:34.530409
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed89d0988d09'
down_revision = 'd7ac53a809c1'
branch_labels = None
depends_on = None


def upgrade():
    """Пройти сохранённую ревизию в линейной истории без изменения схемы."""
    pass


def downgrade():
    """Откатить отметку сохранённой ревизии без изменения схемы."""
    pass
