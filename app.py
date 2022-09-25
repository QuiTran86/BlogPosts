from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from infrastructure import db
from resources.auth import auth as auth_blueprint

from config import config


def create_app(env_config):
    app = Flask(__name__)
    app.config.from_object(config[env_config])
    Bootstrap().init_app(app)
    Moment().init_app(app)
    db.init_app(app)
    app.register_blueprint(auth_blueprint)
    return app
