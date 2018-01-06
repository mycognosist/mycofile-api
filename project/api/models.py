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
    dimensions = db.Column(db.String(32), index=True)
    substrate = db.Column(db.String(64), index=True)
    treatment = db.Column(db.String(64), index=True)
    timestamp = db.Column(
        db.DateTime(),
        default=datetime.datetime.utcnow,
        index=True
    )
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('lines.id'))
    active = db.Column(db.Boolean, default=True)
    contam = db.Column(db.Boolean, default=False)
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
