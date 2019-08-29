from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_api(config_class=Config):
    api = Flask(__name__)
    api.config.from_object(config_class)

    db.init_app(api)
    migrate.init_app(api, db=db)
