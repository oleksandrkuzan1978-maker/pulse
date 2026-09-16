"""Создать приложение Flask и запустить сервер при прямом вызове модуля."""

from app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
