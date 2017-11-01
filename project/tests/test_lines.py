# project/tests/test_lines.py


import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Line
from project.tests.utils import add_line


class TestLineService(BaseTestCase):
    """Tests for the Lines Service."""

    def test_add_line(self):
        """Ensure a new line action can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/lines',
                data=json.dumps(dict(
                    container='Petri',
                    substrate='LME',
                    culture_id='GLJP001',
                    user_id=1
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('Line object was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_line_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/api/lines',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_line_invalid_culture_id_keys(self):
        """Ensure error is thrown if the JSON object does not have a culture_id key."""
        with self.client:
            response = self.client.post(
                '/api/lines',
                data=json.dumps(dict(
                    container='Jar',
                    substrate='Wheat grain',
                    user_id=1
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_line_invalid_user_id_keys(self):
        """Ensure error is thrown if the JSON object does not have a user_id key."""
        with self.client:
            response = self.client.post(
                '/api/lines',
                data=json.dumps(dict(
                    container='Jar',
                    substrate='Wheat grain',
                    culture_id='PCMA002'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

def test_single_line(self):
        """Ensure get single line object behaves correctly."""
        line = add_line('Petri', 'LME', 'GLJP001', 1)
        with self.client:
            response = self.client.get(f'/api/lines/{line.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Petri', data['data']['container'])
            self.assertIn('LME', data['data']['substrate'])
            self.assertIn('GLJP001', data['data']['culture_id'])
            self.assertEqual(data['data']['user_id'], 1)
            self.assertIn('success', data['status'])
