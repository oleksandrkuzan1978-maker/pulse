# Импортируем Blueprint из Flask.
# Blueprint позволяет объединить связанные маршруты в отдельный модуль.
from flask import Blueprint


# Создаём Blueprint для работы с вопросами.
#
# 'questions' — внутреннее имя Blueprint.
# __name__ — имя текущего Python-модуля.
# url_prefix='/questions' — общий префикс для всех маршрутов
# этого Blueprint.
questions_bp = Blueprint(
    'questions',
    __name__,
    url_prefix='/questions'
)


# Маршрут для получения списка всех вопросов.
#
# Так как выше установлен url_prefix='/questions',
# полный адрес этого маршрута будет:
# /questions
#
# methods=['GET'] означает, что маршрут отвечает на GET-запрос.
@questions_bp.route('', methods=['GET'])
def get_questions():
    pass


# Маршрут для создания нового вопроса.
#
# Полный адрес:
# /questions
#
# POST используется для отправки данных на сервер
# с целью создания нового объекта.
@questions_bp.route('', methods=['POST'])
def create_question():
    pass


# Маршрут для удаления конкретного вопроса.
#
# <int:id> — переменная часть URL.
# Например:
# /questions/5
#
# Flask возьмёт число 5 из URL и передаст его
# в функцию как аргумент id.
@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    pass


# Маршрут для изменения конкретного вопроса.
#
# Например:
# /questions/5
#
# PUT и PATCH используются для изменения существующего объекта.
@questions_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_question(id):
    pass


# Маршрут для получения одного конкретного вопроса.
#
# Например:
# GET /questions/5
#
# Flask передаст число 5 в функцию как id=5.
@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    pass