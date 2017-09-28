# project/api/views.py


from flask import Blueprint, jsonify


cultures_blueprint = Blueprint('cultures', __name__)


@cultures_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
