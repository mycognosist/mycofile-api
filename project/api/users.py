# project/api/users.py


from flask import Blueprint, jsonify, make_response, request, render_template

from project.api.models import User
from project.api.utils import authenticate, is_admin
from project import db

from sqlalchemy import exc

users_blueprint = Blueprint('users', __name__)


@users_blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found.'}), 404)


# add a new user
@users_blueprint.route('/api/users', methods=['POST'])
@authenticate
def add_user(resp):
    if not is_admin(resp):
        response_object = {
            'status': 'fail',
            'message': 'You do not have permission to do that.'
        }
        return jsonify(response_object), 401
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(
                username=username,
                email=email,
                password=password
            ))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


# display a single user
@users_blueprint.route('/api/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details."""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist.'
    }
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


# display all users
@users_blueprint.route('/api/users', methods=['GET'])
def get_all_users():
    """Get all users."""
    users = User.query.all()
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        users_list.append(user_object)
    response_object = {
        'status': 'success',
        'data': {
            'users': users_list
        }
    }
    return jsonify(response_object), 200
