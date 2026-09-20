"""Предоставить фабрику Flask с расширениями базы данных и маршрутами вопросов."""

import os
from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routers import questions_bp, answers_bp, categories_bp
CONFIG_MAP = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
}

migrate = Migrate()

def create_app(config_object=None):
    """Создать приложение, подключить расширения и маршруты вопросов.

    Args:
        config_object: Объект конфигурации или строка с путём импорта.
            Если не задан, конфигурация выбирается по APP_ENV;
            значение по умолчанию — development.

    Returns:
        Экземпляр Flask с SQLAlchemy, Flask-Migrate и Blueprint вопросов.

    Raises:
        KeyError: Значение APP_ENV отсутствует в CONFIG_MAP.
    """
    app = Flask(__name__)

    if config_object is None:
        mode = os.environ.get('APP_ENV', 'development')
        config_object = CONFIG_MAP[mode]

    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(questions_bp)
    app.register_blueprint(answers_bp)
    app.register_blueprint(categories_bp)

    return app