from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.models import db


class Question(db.Model):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(db.String(255))
    answers: Mapped[list['Answer']] = relationship(back_populates='question')


