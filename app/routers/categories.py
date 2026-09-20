"""Обработать создание, чтение списка, переименование и удаление категорий."""
from flask import Blueprint, jsonify, request
from app.models import Category, db
from app.schemas.questions import CategoryCreate, CategoryRead, CategoryUpdate, CategoriesList
from pydantic import ValidationError


categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


def _get_category_or_404(category_id: int):
    """Вернуть (Category, None) либо (None, кортеж JSON-ответа с кодом 404)."""
    category = db.session.get(Category, category_id)
    if category is None:
        return None, (jsonify({"error": f"Category with id={category_id} not found"}), 404,)
    return category, None


@categories_bp.route('', methods=['POST'])
def create_categories():
    """Создать одну категорию из обязательного поля name в POST /categories.

    Возвращает JSON категории и 201; неразобранное тело или JSON null — 400,
    нарушение схемы — 422. Пробелы по краям имени удаляет схема.
    Уникальность названия не проверяется; ошибки БД не перехватываются.
    """
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
    try:
        category_in = CategoryCreate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({"errors":"Validation error",
                        "messages": exc.errors()}), 422
    category = Category(name=category_in.name)
    db.session.add(category)
    db.session.commit()
    return jsonify(CategoryRead.model_validate(category).model_dump()), 201


@categories_bp.route('', methods=['GET'])
def get_categories():
    """Вернуть проверенный JSON-список категорий и 200; при отсутствии данных — []."""
    categories = db.session.scalars(db.select(Category))
    result = CategoriesList.dump_python(CategoriesList.validate_python(categories))
    return jsonify(result), 200


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id: int):
    """Удалить категорию, её вопросы и ответы через ORM-каскады.

    Args:
        category_id: Идентификатор удаляемой категории.

    Returns:
        Пустое тело и 204 либо JSON ошибки и 404, если категории нет.

    Ошибки сохранения в БД не перехватываются.
    """
    category, error = _get_category_or_404(category_id)
    if error:
        return error
    db.session.delete(category)
    db.session.commit()
    return "", 204


@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id: int):
    """Переименовать категорию по обязательному полю name в PUT-запросе.

    Args:
        category_id: Идентификатор изменяемой категории.

    Returns:
        JSON категории и 200, JSON ошибки и 404 при отсутствии категории,
        400 при неразобранном теле или null, 422 при нарушении схемы.

    Дополнительные поля запрещены. Ошибки БД не перехватываются.
    """
    category, error = _get_category_or_404(category_id)
    if error:
        return error
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Invalid or mossing JSON body"}), 400
    try:
        category_in = CategoryUpdate.model_validate(payload)
    except ValidationError as exc:
        return jsonify({'errors': "Validation error",
                        "details": exc.errors(),}), 422
    category.name = category_in.name
    db.session.commit()
    return jsonify(CategoryRead.model_validate(category).model_dump()), 200