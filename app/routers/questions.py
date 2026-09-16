"""Объявить Blueprint вопросов с пока не реализованными обработчиками."""

from flask import Blueprint


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


@questions_bp.route('', methods=['GET'])
def get_questions():
    """Обозначить GET /questions; заглушка возвращает None вместо HTTP-ответа."""
    pass

@questions_bp.route('', methods=['POST'])
def create_question():
    """Обозначить POST /questions; заглушка возвращает None вместо HTTP-ответа."""
    pass

@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Обозначить DELETE /questions/<id>; обработчик пока не реализован.

    Args:
        id: Идентификатор вопроса из URL.

    Returns:
        None: Заглушка пока не формирует HTTP-ответ.
    """
    pass

@questions_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_question(id):
    """Обозначить PUT или PATCH /questions/<id>; обработчик пока не реализован.

    Args:
        id: Идентификатор вопроса из URL.

    Returns:
        None: Заглушка пока не формирует HTTP-ответ.
    """
    pass

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Обозначить GET /questions/<id>; обработчик пока не реализован.

    Args:
        id: Идентификатор вопроса из URL.

    Returns:
        None: Заглушка пока не формирует HTTP-ответ.
    """
    pass