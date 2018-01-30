# project/api/lines.py


from flask import Blueprint, jsonify, make_response, request

from project.api.models import Line
from project import db

from sqlalchemy import exc

lines_blueprint = Blueprint('lines', __name__, template_folder='./templates')


@lines_blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found.'}), 404)

# add a line activity
@lines_blueprint.route('/api/v1/lines', methods=['POST'])
def add_line_activity():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    container = post_data.get('container')
    dimensions = post_data.get('dimensions')
    substrate = post_data.get('substrate')
    treatment = post_data.get('treatment')
    parent_id = post_data.get('parent_id')
    culture_id = post_data.get('culture_id')
    try:
        line = Line(
            container=container,
            dimensions=dimensions,
            substrate=substrate,
            treatment=treatment,
            parent_id=parent_id,
            culture_id=culture_id
        )
        line.save()
        response_object = {
            'status': 'success',
            'message': 'Line object was added!'
        }
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

# display a single line object
@lines_blueprint.route('/api/v1/lines/<line_id>', methods=['GET'])
def get_single_line_object(line_id):
    """Get single line object details."""
    response_object = {
        'status': 'fail',
        'message': 'Line object does not exist.'
    }
    try:
        line = Line.query.filter_by(id=line_id).first()
        if not line:
            return jsonify(response_object), 404
        else:
            level = line.level
            response_object = {
                'status': 'success',
                'data': {
                    'id': line.id,
                    'culture_id': line.culture_id,
                    'container': line.container,
                    'dimensions': line.dimensions,
                    'substrate': line.substrate,
                    'treatment': line.treatment,
                    'timestamp': line.timestamp,
                    'parent_id': line.parent_id,
                    'active': line.active,
                    'contam': line.contam,
                    'level': level
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

# display all lines in the library
@lines_blueprint.route('/api/v1/lines', methods=['GET'])
def get_all_lines():
    """Get all line details for user."""
    total_lines = Line.query.count()
    lines = Line.query.all()
    lines_list = []
    for line in lines:
        level = line.level
        line_object = {
            'id': line.id,
            'culture_id': line.culture_id,
            'container': line.container,
            'dimensions': line.dimensions,
            'substrate': line.substrate,
            'treatment': line.treatment,
            'timestamp': line.timestamp,
            'parent_id': line.parent_id,
            'active': line.active,
            'contam': line.contam,
            'level': line.level
        }
        lines_list.append(line_object)
    response_object = {
        'status': 'success',
        'data': {
            'lines': lines_list
        }
    }
    return jsonify(response_object), 200

# delete a line object
@lines_blueprint.route('/api/v1/lines/<line_object_id>', methods=['DELETE'])
def delete_single_line_object(line_object_id):
    """Delete a line object."""
    try:
        line = Line.query.filter_by(id=line_object_id).first()
        if not line:
            response_object = {
                'status': 'fail',
                'message': f'{line_object_id} does not exist.'
            }
            return jsonify(response_object), 404
        else:
            db.session.delete(line)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{line_object_id} was deleted.'
            }
            return jsonify(response_object), 200
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

# update a line object
@lines_blueprint.route('/api/v1/lines/<line_object_id>', methods=['PUT'])
def update_single_line_object(line_object_id):
    """Update an existing line object."""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    active = post_data.get('active')
    contam = post_data.get('contam')
    try:
        line = Line.query.filter_by(id=line_object_id).first()
        if not line:
            response_object = {
                'status': 'fail',
                'message': f'{line_object_id} does not exist.'
            }
            return jsonify(response_object), 404
        else:
            line.active = active
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{line_object_id} was updated.'
            }
            return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
