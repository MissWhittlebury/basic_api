from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_cors

from config import Config


db = SQLAlchemy()
migrate = Migrate()
cors = flask_cors.CORS()


def create_api(config_class=Config):
    api = Flask(__name__)
    api.config.from_object(config_class)

    cors.init_app(api, resources={r"/*": {"origins": "*"}})
    db.init_app(api)
    migrate.init_app(api, db=db)

    from api.routes import bp as main_bp
    api.register_blueprint(main_bp)

    from api import error_handlers
    api.register_error_handler(404, error_handlers.handle_404)


    return api


from api import models
