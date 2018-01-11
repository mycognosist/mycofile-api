# project/api/counts.py
# Query app for various counts (total cultures, total active lines etc.)


from flask import Blueprint, jsonify, make_response, request

from project.api.models import Culture, Line
from project import db

from sqlalchemy import exc

counts_blueprint = Blueprint('counts', __name__, template_folder='./templates')


@counts_blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found.'}), 404)


# return all counts
@counts_blueprint.route('/api/v1/counts', methods=['GET'])
def list_counts():
    """Return various counts for cultures and lines."""
    total_cultures = Culture.query.count()
    total_lines = Line.query.count()
    response_object = {
        'status': 'success',
        'data': {
            'total_cultures': total_cultures,
            'total_lines': total_lines
        }
    }
    return jsonify(response_object), 200
