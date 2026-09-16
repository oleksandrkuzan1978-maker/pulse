"""Создать расширение SQLAlchemy и зарегистрировать модели приложения."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .questions import Question
from .answers import Answer
from .categories import Category