"""Предоставить общий поиск ORM-объекта с JSON-ответом при его отсутствии."""
from app.models import db
from app.schemas.errors import error_message

def _get_object_or_404(model, pk):
    """Найти объект модели по первичному ключу без возбуждения HTTP-исключения.

    Args:
        model: Класс модели SQLAlchemy.
        pk: Значение первичного ключа.

    Returns:
        (объект, None) либо (None, кортеж JSON-ответа со статусом 404).
    """
    obj = db.session.get(model, pk)
    if obj is None:
        return None, error_message(f'{model.__name__} with id {pk} not found', 404)
    return obj, None

