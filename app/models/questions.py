"""Определить модель вопроса со связями с категорией и ответами."""

from app.models import db
# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from .categories import Category

class Question(db.Model):
    """Вопрос, принадлежащий категории и содержащий ответы.

    Attributes:
        id: Первичный ключ вопроса.
        text: Текст вопроса длиной до 255 символов.
        category_id: Обязательный внешний ключ категории.
        category: Категория вопроса.
        responses: Ответы с каскадным удалением через ORM, включая сироты.
    """

    __tablename__ = 'questions'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    text: db.Mapped[str] = db.mapped_column(db.String(255))
    category_id: db.Mapped[int] = db.mapped_column(db.ForeignKey('categories.id'))
    category: db.Mapped['Category'] = db.relationship(back_populates="questions")
    responses: db.Mapped[list['Answer']] = db.relationship(
        back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self):
        """Вернуть строку с идентификатором и текстом вопроса."""
        return f"<Question {self.id}: {self.text}>"