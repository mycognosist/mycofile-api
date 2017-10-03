# project/api/models.py


import datetime
import jwt
from flask import current_app
from project import db, bcrypt


class Culture(db.Model):
    __tablename__ = "cultures"
    id = db.Column(db.Integer, primary_key=True)
    genus = db.Column(db.String(64), index=True)
    species = db.Column(db.String(64), index=True)
    strain = db.Column(db.String(64), index=True)
    unique_id = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Culture %r>' % (self.unique_id)

    def __init__(self, genus, species, strain, unique_id):
        self.genus = genus
        self.species = species
        self.strain = strain
        self.unique_id = unique_id


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(128),
        index=True,
        unique=True,
        nullable=False
    )
    email = db.Column(
        db.String(128),
        index=True,
        unique=True,
        nullable=False
    )
    active = db.Column(db.Boolean(), default=True)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    def encode_auth_token(self, user_id):
        """Generates the auth token."""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    def __repr__(self):
        return '<User %r>' % (self.username)
