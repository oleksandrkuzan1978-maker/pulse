"""Определить модель ответа на вопрос."""

from app.models import db

class Answer(db.Model):
    """Ответ, выражающий согласие или несогласие с вопросом.

    Attributes:
        id: Первичный ключ ответа.
        question_id: Внешний ключ вопроса.
        is_agree: Признак согласия с вопросом.
        question: Вопрос, к которому относится ответ.
    """

    __tablename__ = 'answers'

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    question_id: db.Mapped[int] = db.mapped_column(db.ForeignKey('questions.id'))
    is_agree: db.Mapped[bool]

    question: db.Mapped["Question"] = db.relationship(back_populates="responses")

    def __repr__(self):
        """Вернуть строку с идентификаторами ответа и вопроса и признаком согласия."""
        return f"<Answer {self.id}: question={self.question_id}, is_agree={self.is_agree}>"