# project/api/views.py


from flask import Blueprint, jsonify, make_response, request, render_template

from project.api.models import Culture
from project import db

from sqlalchemy import exc

cultures_blueprint = Blueprint('cultures', __name__, template_folder='./templates')


@cultures_blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found.'}), 404)


# system status
@cultures_blueprint.route('/api/v1/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


# add a new culture to the library
@cultures_blueprint.route('/api/v1/cultures', methods=['POST'])
def add_culture():
    post_data = request.get_json()
    if not post_data or post_data.get('unique_id') == None:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    genus = post_data.get('genus')
    species = post_data.get('species')
    strain = post_data.get('strain')
    culture_id = post_data.get('unique_id')
    try:
        culture = Culture.query.filter_by(culture_id=culture_id).first()
        if not culture:
            db.session.add(Culture(
                genus=genus,
                species=species,
                strain=strain,
                culture_id=culture_id
            ))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{culture_id} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That culture_id already exists.'
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
@cultures_blueprint.route(
    '/api/v1/cultures/<culture_id>',
    methods=['GET']
)

def get_single_culture(culture_id):
    """Get single culture details for specified user."""
    response_object = {
        'status': 'fail',
        'message': 'Culture does not exist.'
    }
    try:
        culture = Culture.query.filter_by(culture_id=culture_id).first()
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
                    'culture_id': culture.culture_id
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

# display all cultures in the library
@cultures_blueprint.route('/api/v1/cultures', methods=['GET'])
def get_all_cultures():
    """Get all culture details."""
    total_cultures = Culture.query.count()
    cultures = Culture.query.all()
    cultures_list = []
    for culture in cultures:
        culture_object = {
            'id': culture.id,
            'genus': culture.genus,
            'species': culture.species,
            'strain': culture.strain,
            'culture_id': culture.culture_id
        }
        cultures_list.append(culture_object)
    count = {'total_cultures': total_cultures}
    cultures_list.append(count)
    response_object = {
        'status': 'success',
        'data': {
            'cultures': cultures_list
        }
    }
    return jsonify(response_object), 200

# delete a culture
@cultures_blueprint.route('/api/v1/cultures/<culture_id>',
                           methods=['DELETE'])
def delete_single_culture(culture_id):
    """Delete a culture."""
    try:
        culture = Culture.query.filter_by(culture_id=culture_id).first()
        if not culture:
            response_object = {
                'status': 'fail',
                'message': f'{culture_id} does not exist.'
            }
            return jsonify(response_object), 404
        else:
            db.session.delete(culture)
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{culture_id} was deleted.'
            }
            return jsonify(response_object), 200
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

# update a culture
@cultures_blueprint.route('/api/v1/cultures/<culture_id>', methods=['PUT'])
def update_single_culture(culture_id):
    """Update an existing culture."""
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    genus = post_data.get('genus')
    species = post_data.get('species')
    strain = post_data.get('strain')
    try:
        culture = Culture.query.filter_by(culture_id=culture_id).first()
        if not culture:
            response_object = {
                'status': 'fail',
                'message': f'{culture_id} does not exist.'
            }
            return jsonify(response_object), 404
        else:
            culture.genus = genus
            culture.species = species
            culture.strain = strain
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{culture_id} was updated.'
            }
            return jsonify(response_object), 201
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
