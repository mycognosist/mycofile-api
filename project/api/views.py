# project/api/views.py


from flask import Blueprint, jsonify, make_response, request

from project.api.models import Culture
from project import db

cultures_blueprint = Blueprint('cultures', __name__)


@cultures_blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# system status
@cultures_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


# add a new culture to the library
@cultures_blueprint.route('/api/cultures', methods=['POST'])
def add_culture():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    if not post_data.get('unique_id'):
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    genus = post_data.get('genus')
    species = post_data.get('species')
    strain = post_data.get('strain')
    unique_id = post_data.get('unique_id')
    try:
        culture = Culture.query.filter_by(unique_id=unique_id).first()
        if not culture:
            db.session.add(Culture(
                genus=genus,
                species=species,
                strain=strain,
                unique_id=unique_id
            ))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{unique_id} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That unique id already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


# display a single culture from the library
@cultures_blueprint.route('/api/cultures/<unique_id>', methods=['GET'])
def get_single_culture(unique_id):
    """Get single culture details."""
    response_object = {
        'status': 'fail',
        'message': 'Culture does not exist.'
    }
    try:
        culture = Culture.query.filter_by(unique_id=unique_id).first()
        if not culture:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': culture.id,
                    'genus': culture.genus,
                    'species': culture.species,
                    'strain': culture.strain,
                    'unique_id': culture.unique_id
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

# display all cultures in the library
@cultures_blueprint.route('/api/cultures', methods=['GET'])
def get_all_cultures():
    """Get all culture details."""
    cultures = Culture.query.all()
    cultures_list = []
    for culture in cultures:
        culture_object = {
            'id': culture.id,
            'genus': culture.genus,
            'species': culture.species,
            'strain': culture.strain,
            'unique_id': culture.unique_id
        }
        cultures_list.append(culture_object)
    response_object = {
        'status': 'success',
        'data': {
            'cultures': cultures_list
        }
    }
    return jsonify(response_object), 200
