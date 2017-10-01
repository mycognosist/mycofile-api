# project/__init__.py


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


# instantiate the db
db = SQLAlchemy()

# instantiate flask migrate
migrate = Migrate()

# instantiate flask bcrypt
bcrypt = Bcrypt()


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app.config.from_object('project.config')

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.views import cultures_blueprint, users_blueprint
    app.register_blueprint(cultures_blueprint)
    app.register_blueprint(users_blueprint)

    return app
