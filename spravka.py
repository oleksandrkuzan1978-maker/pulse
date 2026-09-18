"""Вывести справку по Flask Blueprint при запуске или импорте модуля."""

from flask import Blueprint
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
#print(dir(mapped_column))
help(Blueprint)