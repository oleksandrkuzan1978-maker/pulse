"""Объединить две ветви истории миграций без изменения схемы.


Revision ID: ed89d0988d09
Revises: d7ac53a809c1, f7f26ce384b9
Create Date: 2026-09-16 15:04:34.530409
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed89d0988d09'
down_revision = ('d7ac53a809c1', 'f7f26ce384b9')
branch_labels = None
depends_on = None


def upgrade():
    """Обозначить слияние ветвей; не выполнять операций со схемой."""
    pass


def downgrade():
    """Обозначить откат слияния; не выполнять операций со схемой."""
    pass
