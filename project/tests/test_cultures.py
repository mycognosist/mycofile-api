# project/tests/test_cultures.py


import json

from project.tests.base import BaseTestCase


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

