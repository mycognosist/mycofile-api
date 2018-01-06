# project/tests/utils.py


from project import db
from project.api.models import Culture, Line


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

def add_line(container, substrate, culture_id, parent_id):
    """Helper function to create test lines more easily."""
    line = Line(
        container=container,
        substrate=substrate,
        culture_id=culture_id,
        parent_id=parent_id
    )
    line.save()
    return line
