from flask import Flask

from config import Config


def create_api(config_class=config_class):
    api = Flask(__name__)
    api.config.from_object(config_class)
