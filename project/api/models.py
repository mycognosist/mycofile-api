# project/api/models.py


import datetime
import jwt
from flask import current_app
from project import db, bcrypt


class Line(db.Model):
    _N = 3
    __tablename__ = "lines"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    container = db.Column(db.String(32), index=True)
    substrate = db.Column(db.String(64), index=True)
    timestamp = db.Column(
        db.DateTime(),
        default=datetime.datetime.utcnow,
        index=True
    )
    signature = db.Column(
        db.String(256),
        index=True,
        unique=True
    )
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('lines.id'))
    active = db.Column(db.Boolean, default=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    culture_id = db.Column(
        db.String(32),
        db.ForeignKey('cultures.culture_id'),
        nullable=False
    )
    expansions = db.relationship(
        'Line',
        backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Line %r>' % (self.id)

    def save(self):
        db.session.add(self)
        db.session.commit()
        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)
        db.session.commit()

    def level(self):
        return len(self.path) # self._n - 1


class Culture(db.Model):
    __tablename__ = "cultures"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genus = db.Column(db.String(64), index=True, nullable=False)
    species = db.Column(db.String(64), index=True, nullable=False)
    strain = db.Column(db.String(64), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    culture_id = db.Column(
        db.String(64),
        index=True,
        unique=True
    )

    def __repr__(self):
        return '<Culture %r>' % (self.culture_id)

    def __init__(self, genus, species, strain, culture_id, user_id):
        self.genus = genus
        self.species = species
        self.strain = strain
        self.user_id = user_id
        self.culture_id = culture_id


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    cultures = db.relationship('Culture', backref='cultivator', lazy='dynamic')
    lines = db.relationship('Line', backref='cultivator', lazy='dynamic')

    def __init__(
            self,
            username,
            email,
            password,
            created_at=datetime.datetime.now()):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.created_at = created_at

    def encode_auth_token(self, user_id):
        """Generates the auth token."""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get(
                        'TOKEN_EXPIRATION_SECONDS'
                    )
                ),
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

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token."""
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config.get('SECRET_KEY')
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return '<User %r>' % (self.username)
