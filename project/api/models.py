# project/api/models.py


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
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    active = db.Column(db.Boolean(), default=True)
    password = db.Column(db.String(255))

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
