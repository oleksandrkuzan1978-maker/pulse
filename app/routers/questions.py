"""Обработать HTTP-запросы чтения, создания, изменения и удаления вопросов.

Blueprint использует префикс /questions. Входные данные и представления
вопросов проверяются схемами Pydantic; изменения сохраняются через
сессию SQLAlchemy. Ошибки базы данных в обработчиках не перехватываются.
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import select
from sqlalchemy.orm import joinedload
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
    """Вернуть (Question, None) либо (None, кортеж JSON-ответа с кодом 404)."""
    question = db.session.get(Question, question_id)
    if question is None:
        return None, (jsonify({"error": f"Question with id={question_id} not found"}), 404,)
    return question, None


@questions_bp.route('', methods=['GET'])
def get_questions():
    """Вернуть JSON-список вопросов с вложенными категориями и статусом 200.

    Категории загружаются вместе с вопросами через joinedload. Пустая база
    даёт пустой список. ORM-объекты проверяются схемой QuestionRead.
    """
    questions = db.session.scalars(select(Question).options(joinedload(Question.category)))
    result = QuestionsList.dump_python(QuestionsList.validate_python(questions))
    return jsonify(result), 200


@questions_bp.route('', methods=['POST'])
def create_question():
    """Создать вопрос по text и ID существующей категории из POST /questions.

    Возвращает JSON вопроса с вложенной категорией и статус 201.
    Некорректное или отсутствующее JSON-тело, включая null и неверный
    Content-Type, даёт 400; нарушение схемы — 422; неизвестная категория — 404.
    Новая категория здесь не создаётся. Ошибки БД при commit и ошибки
    валидации представления сохранённого вопроса не перехватываются.
    """
    # Flask берёт тело HTTP-запроса и пытается превратить JSON в Python-объект
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    try:
        # Проверяем данные через Pydantic.
        # Cоответствует ли полученный словарь схеме QuestionCreate?
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
    """Удалить вопрос и связанные ответы через ORM-каскад.

    Args:
        question_id: Идентификатор вопроса из URL.

    Returns:
        Пустое тело и статус 204 либо JSON ошибки со статусом 404.
    """
    question, error = _get_question_or_404(question_id)
    if error:
        return error

    db.session.delete(question)
    db.session.commit()
    return "", 204


@questions_bp.route('/<int:question_id>', methods=['PUT', 'PATCH'])
def update_question(question_id: int):
    """Изменить только текст существующего вопроса через PUT или PATCH.

    Оба метода требуют непустой text; null и дополнительные поля запрещены.
    Сначала проверяется наличие вопроса. Ответы: 404 при его отсутствии,
    400 при неразобранном JSON-теле или null, 422 при нарушении схемы,
    200 с вопросом и вложенной категорией после сохранения.

    Args:
        question_id: Идентификатор обновляемого вопроса.

    Ошибки БД при commit не перехватываются.
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
                        "details": exc.errors(), }), 422
    question.text = question_in.text
    db.session.commit()
    return jsonify(QuestionRead.model_validate(question).model_dump()), 200


@questions_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id: int):
    """Вернуть вопрос с вложенной категорией и статусом 200 либо JSON 404.

    Args:
        question_id: Идентификатор вопроса из URL.

    Данные ORM проверяются схемой QuestionRead перед сериализацией.
    """
    question, error = _get_question_or_404(question_id)
    if error:
        return error

    return jsonify(QuestionRead.model_validate(question).model_dump()), 200
