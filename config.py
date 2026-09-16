"""Загрузить переменные окружения и определить настройки приложения Flask."""

import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Общие настройки приложения из окружения с резервными значениями."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-insecure-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Настройки разработки с включённым режимом отладки."""

    DEBUG = True


class TestingConfig(Config):
    """Настройки приложения с включённым режимом тестирования."""

    TESTING = True


class ProductionConfig(Config):
    """Настройки рабочего окружения, наследующие общую конфигурацию."""

    pass