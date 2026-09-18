"""Обработать HTTP-запросы чтения, создания, изменения и удаления вопросов.

Blueprint использует префикс /questions. Входные данные и представления
вопросов проверяются схемами Pydantic; изменения сохраняются через
сессию SQLAlchemy. Ошибки базы данных в обработчиках не перехватываются.
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import select
from app.models import Question, db
from app.schemas.questions import QuestionRead, QuestionCreate, QuestionsList, QuestionUpdate
from pydantic import ValidationError
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


# @questions_bp.route('', methods=['GET'])
# def get_questions():
#     """Получение списка всех вопросов."""
#     questions = db.session.scalars(select(Question))
#     result = [QuestionRead.model_validate(q).model_dump() for q in questions]
#     return jsonify(result), 200


@questions_bp.route('', methods=['GET'])
def get_questions():
    """Вернуть все вопросы в ответ на GET /questions.

    Returns:
        Кортеж из JSON-ответа со списком вопросов и HTTP-статуса 200.
        При отсутствии вопросов список пуст.

    Raises:
        ValidationError: Данные из базы не соответствуют схеме QuestionRead.
    """
    questions = db.session.scalars(select(Question))
    result = QuestionsList.dump_python(QuestionsList.validate_python(questions))
    return jsonify(result), 200


@questions_bp.route('', methods=['POST'])
def create_question():
    """Проверить JSON запроса и сохранить новый вопрос.

    Текст берётся из тела POST /questions и проверяется схемой QuestionCreate.
    Текущая реализация создаёт Question только с текстом, без category_id.

    Returns:
        Кортеж из JSON-ответа с созданным вопросом и HTTP-статуса 201
        либо JSON-ответа с ошибками входных данных и статуса 422.

    Raises:
        BadRequest: Тело запроса содержит некорректный JSON.
        UnsupportedMediaType: Тип содержимого запроса не соответствует JSON.
        sqlalchemy.exc.IntegrityError: Сохранение нарушает ограничения базы,
            в частности обязательность category_id при отсутствии значения.
        ValidationError: Сохранённый вопрос не соответствует схеме чтения.
    """
    try:
        #Flask берёт тело HTTP-запроса и пытается превратить JSON в Python-объект
        data = request.get_json(silent=True)
        # Проверяем данные через Pydantic.
        #Cоответствует ли полученный словарь схеме QuestionCreate?
        question = QuestionCreate.model_validate(data)
    except ValidationError as e:
        return jsonify({"errors":e.errors()}), 422
    question = Question(text=question.text)
    db.session.add(question)
    db.session.commit()
    return jsonify(QuestionRead.model_validate(question).model_dump()), 201


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удалить вопрос по идентификатору и сохранить изменения.

    Args:
        id: Идентификатор вопроса из URL DELETE /questions/<id>.

    Returns:
        Кортеж из пустой строки и HTTP-статуса 204 при удалении
        либо JSON-ответа с ошибкой и статуса 404, если вопрос не найден.

    Связанные ответы удаляются согласно каскадным настройкам модели Question.
    """
    question = db.session.get(Question, id)
    if not question:
        return jsonify({"errors": "Question not found"}), 404
    db.session.delete(question)
    db.session.commit()
    return  "", 204


@questions_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_question(id):
    """Изменить текст вопроса по запросу PUT или PATCH.

    Оба метода требуют поле text. Отсутствующее или некорректное JSON-тело
    преобразуется в пустой словарь и не проходит проверку обязательного текста.

    Args:
        id: Идентификатор вопроса из URL.

    Returns:
        Кортеж из JSON-ответа и HTTP-статуса: 200 с обновлённым вопросом,
        404 при отсутствии вопроса или 422 при ошибке входных данных.

    Raises:
        ValidationError: Сохранённый вопрос не соответствует схеме чтения.
    """
    question = db.session.get(Question, id)
    if not question:
        return jsonify({"errors": "Question not found"}), 404
    payload = request.get_json(silent=True) or {}
    try:
        q = QuestionUpdate.model_validate(payload)
    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 422
    question.text = q.text
    db.session.commit()
    return jsonify(QuestionRead.model_validate(question).model_dump()), 200


@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    """Вернуть вопрос по идентификатору в ответ на GET /questions/<id>.

    Args:
        id: Идентификатор вопроса из URL.

    Returns:
        Кортеж из JSON-ответа с вопросом и HTTP-статуса 200
        либо JSON-ответа с ошибкой и статуса 404, если вопрос не найден.

    Raises:
        ValidationError: Данные вопроса не соответствуют схеме QuestionRead.
    """
    question = db.session.get(Question, id)
    if not question:
        return  jsonify({"errors":"Question not found"}), 404
    return jsonify(QuestionRead.model_validate(question).model_dump()), 200
