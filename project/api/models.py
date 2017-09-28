# project/api/models.py

from project import db


class Culture(db.Model):
    __tablename__ = "cultures"
    id = db.Column(db.Integer, primary_key=True)
    genus = db.Column(db.String(64), index=True)
    species = db.Column(db.String(64), index=True)
    strain = db.Column(db.String(64), index=True)
    unique_id = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Culture %r>' % (self.unique_id)
