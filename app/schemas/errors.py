"""Формировать JSON-ошибки с сообщением, деталями и заданным HTTP-статусом."""
from pydantic import BaseModel, ValidationError
from flask import jsonify
from pydantic import Field


class ErrorResponse(BaseModel):
    """Тело ошибки: строка error и список details, по умолчанию пустой."""
    error: str
    details: list = Field(default_factory=list)

def error_message(message: str, status_code: int, details: list | None = None):
    """Вернуть пару (JSON-ответ, status_code) для произвольной ошибки.

    Args:
        message: Текст поля error.
        status_code: HTTP-статус ответа.
        details: Детали ошибки; None заменяется пустым списком.
    """
    payload = ErrorResponse(
        error=message,
        details=details if details is not None else [],
    )
    return jsonify(payload.model_dump()), status_code


def validation_error_response(exc: ValidationError, status_code: int):
    """Вернуть JSON ошибки Pydantic и явно переданный HTTP-статус.

    Детали включают тип, расположение, сообщение и входное значение ошибки,
    но не включают URL документации и контекст валидатора.
    """
    payload = ErrorResponse(error='Validation Error', details=exc.errors(include_url=False, include_context=False))
    return jsonify(payload.model_dump()), status_code

# class MyException:
#     @staticmethod
#     def error_message(message: str, status_code: int, details: list | None = None):
#         payload = ErrorResponse(error=message, details=details)
#         return jsonify(payload.model_dump()), status_code
#
#     @staticmethod
#     def validation_error_response(exc: ValidationError, status_code: int):
#         payload = ErrorResponse(error='Validation Error'
#                                 , details=exc.errors(include_url=False, include_context=False))
#         return jsonify(payload.model_dump()), status_code