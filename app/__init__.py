import os

from flask import Flask


CONFIG_MAP = {
    'development': 'config.DevelopmentConfig',
    'testing': 'config.TestingConfig',
    'production': 'config.ProductionConfig',
}


def create_app(config_object=None):
    app = Flask(__name__)

    if config_object is None:
        mode = os.environ.get('APP_ENV', 'development')
        config_object = CONFIG_MAP[mode]

    app.config.from_object(config_object)

    return app