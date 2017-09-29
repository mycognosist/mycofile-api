# project/tests/test_cultures.py


import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Culture

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


class TestCultureService(BaseTestCase):
    """Tests for the Cultures Service."""

    def test_cultures(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_culture(self):
        """Ensure a new culture can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/cultures',
                data=json.dumps(dict(
                    genus='Pholiota',
                    species='nameko',
                    strain='JP',
                    unique_id='PNJP001'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('PNJP001 was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_culture_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/api/cultures',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_culture_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a unique_id key."""
        with self.client:
            response = self.client.post(
                '/api/cultures',
                data=json.dumps(dict(
                    genus='Pholiota',
                    species='nameko',
                    strain='JP'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_culture_duplicate_culture(self):
        """Ensure error is thrown if the unique_id already exists."""
        with self.client:
            self.client.post(
                '/api/cultures',
                data=json.dumps(dict(
                    genus='Pholiota',
                    species='nameko',
                    strain='JP',
                    unique_id='PNJP001'
                )),
                content_type='application/json',
            )
            response = self.client.post(
                '/api/cultures',
                data=json.dumps(dict(
                    genus='Pholiota',
                    species='nameko',
                    strain='JP',
                    unique_id='PNJP001'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That unique id already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_culture(self):
        """Ensure get single culture behaves correctly."""
        culture = add_culture('Pholiota', 'nameko', 'JP', 'PNJP001')
        with self.client:
            response = self.client.get(f'/api/cultures/{culture.unique_id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Pholiota', data['data']['genus'])
            self.assertIn('nameko', data['data']['species'])
            self.assertIn('JP', data['data']['strain'])
            self.assertIn('PNJP001', data['data']['unique_id'])
            self.assertIn('success', data['status'])

    def test_single_culture_no_id(self):
        """Ensure error is thrown if a unique id is not provided."""
        with self.client:
            response = self.client.get('/api/cultures/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Culture does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_culture_incorrect_id(self):
        """Ensure error is thrown if the unique id does not exist."""
        with self.client:
            response = self.client.get('/api/cultures/AAA000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Culture does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_cultures(self):
        """Ensure get all cultures behaves correctly."""
        add_culture('Pholiota', 'nameko', 'JP', 'PNJP001')
        add_culture('Hypsizygus', 'tesselatus', 'RL', 'HTRL001')
        with self.client:
            response = self.client.get('/api/cultures')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['cultures']), 2)
            self.assertIn('Pholiota', data['data']['cultures'][0]['genus'])
            self.assertIn('nameko', data['data']['cultures'][0]['species'])
            self.assertIn('JP', data['data']['cultures'][0]['strain'])
            self.assertIn(
                'PNJP001',
                data['data']['cultures'][0]['unique_id']
            )
            self.assertIn(
                'Hypsizygus',
                data['data']['cultures'][1]['genus']
            )
            self.assertIn(
                'tesselatus',
                data['data']['cultures'][1]['species']
            )
            self.assertIn('RL', data['data']['cultures'][1]['strain'])
            self.assertIn(
                'HTRL001',
                data['data']['cultures'][1]['unique_id']
            )
            self.assertIn('success', data['status'])

    def test_main_no_cultures(self):
        """Ensure the main route behaves correctly when no cultures have been added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Cultures</h1>', response.data)
        self.assertIn(b'<p>No cultures!</p>', response.data)

    def test_main_with_cultures(self):
        """Ensure the main route behaves correctly when cultures have been added to the database."""
        add_culture('Pholiota', 'nameko', 'JP', 'PNJP001')
        add_culture('Hericium', 'erinaceus', 'RL', 'HERL001')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Cultures</h1>', response.data)
        self.assertNotIn(b'<p>No cultures!</p>', response.data)
        self.assertIn(b'<strong>PNJP001</strong>', response.data)
        self.assertIn(b'<strong>HERL001</strong>', response.data)

    def test_main_add_culture(self):
        """Ensure a new culture can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(
                    genus='Lentinula',
                    species='edodes',
                    strain='JP',
                    unique_id='LEJP001'
                ),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Cultures</h1>', response.data)
            self.assertNotIn(b'<p>No cultures!</p>', response.data)
            self.assertIn(b'<strong>LEJP001</strong>', response.data)
