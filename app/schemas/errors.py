from pydantic import BaseModel, ValidationError
from flask import jsonify
from pydantic import Field


class ErrorResponse(BaseModel):
    error: str
    details: list = Field(default_factory=list)

def error_message(message: str, status_code: int, details: list | None = None):
    payload = ErrorResponse(
        error=message,
        details=details if details is not None else [],
    )
    return jsonify(payload.model_dump()), status_code


def validation_error_response(exc: ValidationError, status_code: int):
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