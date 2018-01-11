# project/__init__.py


import os

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate


# instantiate the db
db = SQLAlchemy()

# instantiate flask migrate
migrate = Migrate()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.cultures import cultures_blueprint
    from project.api.lines import lines_blueprint
    from project.api.counts import counts_blueprint
    app.register_blueprint(cultures_blueprint)
    app.register_blueprint(lines_blueprint)
    app.register_blueprint(counts_blueprint)

    return app
