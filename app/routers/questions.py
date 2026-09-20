"""Обработать HTTP-запросы чтения, создания, изменения и удаления вопросов.

Blueprint использует префикс /questions. Входные данные и представления
вопросов проверяются схемами Pydantic; изменения сохраняются через
сессию SQLAlchemy. Ошибки базы данных в обработчиках не перехватываются.
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import select
from app.models import Question, Category, db
from app.schemas.questions import QuestionRead, QuestionCreate, QuestionsList, QuestionUpdate
from pydantic import ValidationError


questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


# @questions_bp.route('', methods=['GET'])
# def get_questions():
#     """Получение списка всех вопросов."""
#     questions = db.session.scalars(select(Question))
#     result = [QuestionRead.model_validate(q).model_dump() for q in questions]
#     return jsonify(result), 200

def _get_question_or_404(question_id: int):
    question = db.session.get(Question, question_id)
    if question is None:
        return None, (jsonify({"error": f"Question with id={question_id} not found"}), 404,)
    return question, None

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
    # Flask берёт тело HTTP-запроса и пытается превратить JSON в Python-объект
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing LSON body"}), 400
    try:
        # Проверяем данные через Pydantic.
        #Cоответствует ли полученный словарь схеме QuestionCreate?
        question_in = QuestionCreate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({"errors": "Validation error",
                        "messages": exc.errors()}), 422

    category = db.session.get(Category, question_in.category_id)

    if category is None:
        return jsonify({
            "error": "Category not found",
            "category_id": question_in.category_id
        }), 404

    question = Question(text=question_in.text,
                        category_id=question_in.category_id)

    db.session.add(question)
    db.session.commit()
    return jsonify(QuestionRead.model_validate(question).model_dump()), 201


@questions_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id: int):
    """Удалить вопрос по идентификатору и сохранить изменения.

    Args:
        id: Идентификатор вопроса из URL DELETE /questions/<id>.

    Returns:
        Кортеж из пустой строки и HTTP-статуса 204 при удалении
        либо JSON-ответа с ошибкой и статуса 404, если вопрос не найден.

    Связанные ответы удаляются согласно каскадным настройкам модели Question.
    """
    question, error = _get_question_or_404(question_id)
    if error:
        return error

    db.session.delete(question)
    db.session.commit()
    return  "", 204


@questions_bp.route('/<int:question_id>', methods=['PUT', 'PATCH'])
def update_question(question_id: int):
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
    question, error = _get_question_or_404(question_id)
    if error:
        return error
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or mossing JSON body"}), 400
    try:
        question_in = QuestionUpdate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({'errors': "Validation error",
                        "details": exc.errors(),}), 422
    question.text = question_in.text
    db.session.commit()
    return jsonify(QuestionRead.model_validate(question).model_dump()), 200


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id: int):
    """Вернуть вопрос по идентификатору в ответ на GET /questions/<id>.

    Args:
        id: Идентификатор вопроса из URL.

    Returns:
        Кортеж из JSON-ответа с вопросом и HTTP-статуса 200
        либо JSON-ответа с ошибкой и статуса 404, если вопрос не найден.

    Raises:
        ValidationError: Данные вопроса не соответствуют схеме QuestionRead.
    """
    question, error = _get_question_or_404(question_id)
    if error:
        return error

    return jsonify(QuestionRead.model_validate(question).model_dump()), 200
