# project/tests/test_culture_model.py


from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import Culture
from project.tests.base import BaseTestCase
from project.tests.utils import add_culture


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
