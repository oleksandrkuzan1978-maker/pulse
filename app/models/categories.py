"""Определить модель категории вопросов и проверку её названия."""

from sqlalchemy.orm import validates
from app.models import db

class Category(db.Model):
    """Категория, объединяющая несколько вопросов.

    Attributes:
        id: Автоматически формируемый первичный ключ.
        name: Название категории, проверяемое при присваивании через ORM.
        questions: Вопросы, связанные с категорией.
    """

    __tablename__ = 'categories'

    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    name: db.Mapped[str] = db.mapped_column(nullable=False)
    questions: db.Mapped[list['Question']] = db.relationship(back_populates="category")

    @validates("name")
    def validate_name(self, key, name):
        """Проверить, что название содержит непробельные символы.

        Args:
            key: Имя проверяемого атрибута, передаваемое SQLAlchemy.
            name: Строка с названием категории.

        Returns:
            Исходное название без удаления окружающих пробелов.

        Raises:
            ValueError: Название пустое или состоит только из пробельных символов.
        """
        if not name.strip():
            raise ValueError("Название категории не может быть пустым")
        return name

    def __repr__(self):
        """Вернуть строку с идентификатором и названием категории."""
        return f"<Category {self.id}, name={self.name}>"