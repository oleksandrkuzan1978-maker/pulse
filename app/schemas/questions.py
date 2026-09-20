"""Определить схемы проверки и сериализации вопросов.

QuestionText удаляет окружающие пробелы и ограничивает длину текста
диапазоном от 1 до 255 символов. QuestionsList проверяет и сериализует
коллекции вопросов с помощью TypeAdapter для списка QuestionRead.
"""

from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, TypeAdapter, computed_field


QCText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255,
    ),
    Field(description="Text of the question or its category"),
]
CategoryID = Annotated[int, Field(strict=True, gt=0)]


class CategoryBase(BaseModel):
    name: QCText


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: CategoryID


class CategoryUpdate(CategoryBase):
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
    """Данные создания вопроса с обязательным текстом.

    Наследует поле text из QuestionBase. Поле категории в схеме не определено.
    """
    category_id: CategoryID


class QuestionRead(QuestionBase):
    """Представление вопроса для чтения, в том числе из ORM-объекта.

    Attributes:
        text: Текст вопроса, наследуемый из QuestionBase.
        id: Целочисленный идентификатор вопроса.
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    category: CategoryRead


class QuestionUpdate(QuestionBase):
    """Данные изменения вопроса с обязательным текстом.

    Наследует обязательное поле text из QuestionBase. Пустые данные
    не проходят проверку, в том числе при использовании схемы для PATCH.
    """
    model_config = ConfigDict(extra="forbid")
    text: QCText


class QuestionResult(BaseModel):
    question_id: int
    agree_count: int
    disagree_count: int

    @computed_field
    @property
    def total(self) -> int:
        return self.agree_count + self.disagree_count


    @computed_field
    @property
    def is_agree_percentage(self) -> float:
        if not self.total:
            return 0.0
        return round(self.agree_count / self.total * 100, 2)


QuestionsList = TypeAdapter(list[QuestionRead])
CategoriesList = TypeAdapter(list[CategoryRead])
