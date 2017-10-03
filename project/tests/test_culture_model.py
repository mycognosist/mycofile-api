# project/tests/test_culture_model.py


from project import db
from project.api.models import Culture
from project.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError


# helper function to create test cultures more easily
def add_culture(genus, species, strain, unique_id):
    culture = Culture(
        genus=genus,
        species=species,
        strain=strain,
        unique_id=unique_id
    )
    db.session.add(culture)
    db.session.commit()
    return culture


class TestCultureModel(BaseTestCase):

    def test_add_culture(self):
        culture = add_culture('Grifola', 'frondosa', 'UK', 'GFUK001')
        self.assertTrue(culture.id)
        self.assertEqual(culture.genus, 'Grifola')
        self.assertEqual(culture.species, 'frondosa')
        self.assertEqual(culture.strain, 'UK')
        self.assertEqual(culture.unique_id, 'GFUK001')

    def test_add_culture_duplicate_unique_id(self):
        culture = add_culture('Hypsizygus', 'tesselatus', 'RL', 'HTRL001')
        duplicate_culture = Culture(
            genus='test',
            species='testing',
            strain='testy',
            unique_id='HTRL001'
        )
        db.session.add(duplicate_culture)
        self.assertRaises(IntegrityError, db.session.commit)
