from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.models import db
from app.models.questions import Question


class Answer(db.Model):
    __tablename__ = 'answers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_agree: Mapped[bool]
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'))
    question: Mapped[Question] = relationship(back_populates='answers')
