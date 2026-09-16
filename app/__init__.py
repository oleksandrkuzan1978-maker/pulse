"""Предоставить фабрику приложения и настроить расширения базы данных."""

import os

from flask import Flask
from flask_migrate import Migrate
from app.models import db

CONFIG_MAP = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
}

migrate = Migrate()

def create_app(config_object=None):
    """Создать приложение Flask и подключить SQLAlchemy и Flask-Migrate.

    Args:
        config_object: Объект конфигурации или строка с путём импорта.
            Если не задан, конфигурация выбирается по APP_ENV;
            значение по умолчанию — development.

    Returns:
        Настроенный экземпляр Flask.

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

    return app