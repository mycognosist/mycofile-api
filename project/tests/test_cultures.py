# project/tests/test_cultures.py


import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Culture
from project.tests.utils import add_culture


class TestCultureService(BaseTestCase):
    """Tests for the Cultures Service."""

    def test_cultures(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/api/v1/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_culture(self):
        """Ensure a new culture can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/v1/cultures',
                data=json.dumps(dict(
                    genus='Pholiota',
                    species='nameko',
                    strain='JP',
                    unique_id='PNJP001',
                    user_id=1
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
                '/api/v1/cultures',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_culture_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a culture_id key."""
        with self.client:
            response = self.client.post(
                '/api/v1/cultures',
                data=json.dumps(dict(
                    genus='Panaeolus',
                    species='cyanescens',
                    strain='Maui',
                    user_id=1
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_culture_invalid_json_user_keys(self):
        """Ensure error is thrown if the JSON object does not have a user_id key."""
        with self.client:
            response = self.client.post(
                '/api/v1/cultures',
                data=json.dumps(dict(
                    genus='Panaeolus',
                    species='cyanescens',
                    strain='Maui',
                    culture_id='PCMA001'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

#    def test_add_culture_duplicate_culture(self):
#        """Ensure error is thrown if the culture_id already exists."""
#        with self.client:
#            self.client.post(
#                '/api/cultures',
#                data=json.dumps(dict(
#                    genus='Pholiota',
#                    species='nameko',
#                    strain='JP',
#                    culture_id='PNJP001'
#                )),
#                content_type='application/json',
#            )
#            response = self.client.post(
#                '/api/cultures',
#                data=json.dumps(dict(
#                    genus='Pholiota',
#                    species='nameko',
#                    strain='JP',
#                    culture_id='PNJP001'
#                )),
#                content_type='application/json',
#            )
#            data = json.loads(response.data.decode())
#            self.assertEqual(response.status_code, 400)
#            self.assertIn(
#                'Sorry. That culture_id already exists.', data['message'])
#            self.assertIn('fail', data['status'])

    def test_single_culture(self):
        """Ensure get single culture behaves correctly."""
        culture = add_culture('Pholiota', 'nameko', 'JP', 'PNJP001', 1)
        with self.client:
            response = self.client.get(f'/api/v1/users/1/cultures/{culture.culture_id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Pholiota', data['data']['genus'])
            self.assertIn('nameko', data['data']['species'])
            self.assertIn('JP', data['data']['strain'])
            self.assertIn('PNJP001', data['data']['culture_id'])
            self.assertEqual(data['data']['user_id'], 1)
            self.assertIn('success', data['status'])

    def test_single_culture_no_id(self):
        """Ensure error is thrown if a valid culture_id is not provided."""
        with self.client:
            response = self.client.get('/api/v1/users/1/cultures/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Culture does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_culture_incorrect_id(self):
        """Ensure error is thrown if the culture_id does not exist."""
        with self.client:
            response = self.client.get('/api/v1/users/1/cultures/AAA000')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Culture does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_cultures(self):
        """Ensure get all cultures behaves correctly."""
        add_culture('Pholiota', 'nameko', 'JP', 'PNJP001', 1)
        add_culture('Hypsizygus', 'tesselatus', 'RL', 'HTRL001', 1)
        with self.client:
            response = self.client.get('/api/v1/users/1/cultures')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['cultures']), 2)
            self.assertIn('Pholiota', data['data']['cultures'][0]['genus'])
            self.assertIn('nameko', data['data']['cultures'][0]['species'])
            self.assertIn('JP', data['data']['cultures'][0]['strain'])
            self.assertEqual(data['data']['cultures'][0]['user_id'], 1)
            self.assertIn(
                'PNJP001',
                data['data']['cultures'][0]['culture_id']
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
            self.assertEqual(data['data']['cultures'][1]['user_id'], 1)
            self.assertIn(
                'HTRL001',
                data['data']['cultures'][1]['culture_id']
            )
            self.assertIn('success', data['status'])

    def test_delete_culture(self):
        """Ensure culture is successfully deleted."""
        add_culture('Pholiota', 'nameko', 'JP', 'PNJP001', 1)
        with self.client:
            response = self.client.delete(
                '/api/v1/users/1/cultures/PNJP001',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('PNJP001 was deleted.', data['message'])
            self.assertIn('success', data['status'])

    def test_delete_culture_incorrect_culture_id(self):
        """Ensure error is thrown if the culture_id does not exist."""
        with self.client:
            response = self.client.delete(
                '/api/v1/users/1/cultures/ABC123',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('ABC123 does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_culture(self):
        """Ensure culture is successfully updated."""
        add_culture('Pholiota', 'nameko', 'JP', 'PNJP001', 1)
        with self.client:
            response = self.client.put(
                '/api/v1/users/1/cultures/PNJP001',
                data=json.dumps(dict(
                    genus='Pholiota',
                    species='nameko',
                    strain='Taki'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('PNJP001 was updated.', data['message'])
            self.assertIn('success', data['status'])

    def test_update_culture_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.put(
                '/api/v1/users/1/cultures/PNJP001',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_culture_incorrect_culture_id(self):
        """Ensure error is thrown if the culture_id does not exist."""
        with self.client:
            response = self.client.put(
                '/api/v1/users/1/cultures/BBB222',
                data=json.dumps(dict(
                    genus='Pleurotus',
                    species='djamor',
                    strain='Taki'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('BBB222 does not exist.', data['message'])
            self.assertIn('fail', data['status'])
