"""Определить схемы создания и чтения булевых ответов на вопросы.

AnswerCreate требует строгое bool. AnswerRead читает атрибуты ORM.
AnswersList сериализует списки ответов. AnswerText и AnswerId пока
не используются полями этих схем.
"""

from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, TypeAdapter

AnswerText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=255,
    ),
    Field(description="Text of the question"),
]

AnswerId = Annotated[
    int,
    Field(description="ID of the question"),
]


class AnswerBase(BaseModel):
    """Базовая схема ответа без общих полей."""

    pass

class AnswerCreate(AnswerBase):
    """Обязательное строгое булево is_agree; ID вопроса передаётся в URL."""

    is_agree: Annotated[bool, Field(strict=True)]


class AnswerRead(AnswerBase):
    """ID ответа, признак согласия и ID вопроса, включая чтение из ORM."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_agree: bool
    question_id: int

class AnswerUpdate(AnswerBase):
    """Заготовка схемы без полей; маршрута обновления ответов пока нет."""

    pass
    

AnswersList = TypeAdapter(list[AnswerRead])
