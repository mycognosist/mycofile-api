# project/__init__.py


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
    app.config.from_object('project.config')

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.views import cultures_blueprint
    app.register_blueprint(cultures_blueprint)

    return app
