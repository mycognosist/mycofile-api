# project/tests/utils.py


from project import db
from project.api.models import User, Culture


def add_user(username, email, password):
    """Helper function to create test users more easily."""
    user = User(
        username=username,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return user


def add_culture(genus, species, strain, culture_id):
    """Helper function to create test cultures more easily."""
    culture = Culture(
        genus=genus,
        species=species,
        strain=strain,
        culture_id=culture_id
    )
    db.session.add(culture)
    db.session.commit()
    return culture
