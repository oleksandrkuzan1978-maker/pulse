"""Проверять и сериализовать категории, вопросы и результаты голосования.

QCText обрезает окружающие пробелы и допускает 1–255 символов.
CategoryID требует положительный int без преобразования строк и bool.
Схема чтения вопроса включает вложенную категорию; адаптеры обслуживают списки.
"""

from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, computed_field
from typing import Annotated
from pydantic import Field, StringConstraints

QCText = Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=255,
        ),
        Field(description="Text of the question or its category")
    ]

CategoryID = Annotated[int, Field(strict=True, gt=0)]


class CategoryBase(BaseModel):
    """Название категории длиной 1–255 символов после удаления пробелов по краям."""
    name: QCText


class CategoryCreate(CategoryBase):
    """Данные создания категории с обязательным name; лишние поля игнорируются."""
    pass


class CategoryRead(CategoryBase):
    """ID и название категории, читаемые в том числе из атрибутов ORM-объекта."""
    model_config = ConfigDict(from_attributes=True)
    id: CategoryID


class CategoryUpdate(CategoryBase):
    """Обязательное новое название категории; дополнительные поля запрещены."""
    model_config = ConfigDict(extra="forbid")
    name: QCText


class QuestionBase(BaseModel):
    """Общая схема вопроса с обязательным текстом.

    Attributes:
        text: Текст длиной от 1 до 255 символов после удаления
            окружающих пробелов.
    """

    text: QCText


class QuestionCreate(QuestionBase):
    """Данные создания вопроса: text и положительный целочисленный category_id.

    Существование категории проверяет обработчик запроса, а не схема.
    """
    category_id: CategoryID


class QuestionRead(QuestionBase):
    """Представление вопроса с вложенной категорией из словаря или ORM-объекта.

    Attributes:
        text: Текст вопроса, наследуемый из QuestionBase.
        id: Идентификатор вопроса.
        category: Объект категории с её id и name.

    Отдельное поле category_id в ответ не включается.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    category: CategoryRead


class QuestionUpdate(QuestionBase):
    """Обязательный непустой text для PUT/PATCH; null и лишние поля запрещены."""
    model_config = ConfigDict(extra="forbid")
    text: QCText


class QuestionResult(BaseModel):
    """Счётчики ответов на вопрос с вычисляемыми total и is_agree_percentage."""
    question_id: int
    agree_count: int
    disagree_count: int

    @computed_field
    @property
    def total(self) -> int:
        """Вернуть сумму согласий и несогласий."""
        return self.agree_count + self.disagree_count

    @computed_field
    @property
    def is_agree_percentage(self) -> float:
        """Вернуть процент согласий с округлением до сотых; без ответов — 0.0."""
        if not self.total:
            return 0.0
        return round(self.agree_count / self.total * 100, 2)


QuestionsList = TypeAdapter(list[QuestionRead])
CategoriesList = TypeAdapter(list[CategoryRead])
