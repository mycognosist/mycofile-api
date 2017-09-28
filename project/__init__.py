# project/__init__.py


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# instantiate the app
app = Flask(__name__)

# set config
app.config.from_object('project.config')

# instatiate the db
db = SQLAlchemy(app)


from project import models


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
