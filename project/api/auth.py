# project/api/auth.py


from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import exc, or_

from project.api.models import User
from project.api.utils import authenticate
from project import db, bcrypt


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found.'}), 404)


# register a new user
@auth_blueprint.route('/api/auth/register', methods=['POST'])
def register_user():
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
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email==email)).first()
        if not user:
            # add new user to db
            new_user = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That user already exists.'
            }
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


# user login
@auth_blueprint.route('/api/auth/login', methods=['POST'])
def login_user():
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch user data
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return jsonify(response_object), 404
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again.'
        }
        return jsonify(response_object), 500


# user logout
@auth_blueprint.route('/api/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp):
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200

# user status
@auth_blueprint.route('/api/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    user = User.query.filter_by(id=resp).first()
    response_object = {
        'status': 'success',
        'data': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'active': user.active,
            'created_at': user.created_at
        }
    }
    return jsonify(response_object), 200
