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
        l = Line(
            container='Petri',
            substrate='LME',
            culture_id='GLJP001',
            user_id=1
        )
        l.save()
        with self.client:
            response = self.client.get(f'/api/lines/1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Petri', data['data']['container'])
            self.assertIn('LME', data['data']['substrate'])
            self.assertIn('GLJP001', data['data']['culture_id'])
            self.assertEqual(data['data']['user_id'], 1)
            self.assertIn('success', data['status'])

    def test_single_line_no_id(self):
        """Ensure error is thrown if a valid id is not provided."""
        with self.client:
            response = self.client.get('/api/lines/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Line object does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_line_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/api/lines/99')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Line object does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_lines(self):
        """Ensure get all lines behaves correctly."""
        l1 = Line(
            container='Petri',
            substrate='LME',
            culture_id='GLJP001',
            user_id=1
        )
        l2 = Line(
            container='Jar',
            substrate='Wheat',
            culture_id='HETK001',
            user_id=2
        )
        l1.save()
        l2.save()
        with self.client:
            response = self.client.get('/api/lines')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['lines']), 2)
            self.assertIn('Petri', data['data']['lines'][0]['container'])
            self.assertIn('LME', data['data']['lines'][0]['substrate'])
            self.assertIn('GLJP001', data['data']['lines'][0]['culture_id'])
            self.assertEqual(data['data']['lines'][0]['id'], 1)
            self.assertEqual(data['data']['lines'][0]['user_id'], 1)
            self.assertIn('Jar', data['data']['lines'][1]['container'])
            self.assertIn('Wheat', data['data']['lines'][1]['substrate'])
            self.assertIn('HETK001', data['data']['lines'][1]['culture_id'])
            self.assertEqual(data['data']['lines'][1]['id'], 2)
            self.assertEqual(data['data']['lines'][1]['user_id'], 2)
            self.assertIn('success', data['status'])

    def test_delete_line_object(self):
        """Ensure line object is successfully deleted."""
        l1 = Line(
            container='Petri',
            substrate='LME',
            culture_id='GLJP001',
            user_id=1
        )
        l1.save()
        with self.client:
            response = self.client.delete(
                '/api/lines/1',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('1 was deleted.', data['message'])
            self.assertIn('success', data['status'])

    def test_delete_line_object_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.delete(
                '/api/lines/99',
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('99 does not exist.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_line_object(self):
        """Ensure line object is successfully updated."""
        l1 = Line(
            container='Petri',
            substrate='LME',
            culture_id='GLJP001',
            user_id=1,
            active=True
        )
        l1.save()
        with self.client:
            response = self.client.put(
                '/api/lines/1',
                data=json.dumps(dict(
                    active=False
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('1 was updated.', data['message'])
            self.assertIn('success', data['status'])

    def test_update_line_object_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.put(
                '/api/lines/1',
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_line_object_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.put(
                '/api/lines/999',
                data=json.dumps(dict(
                    active=False
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('999 does not exist.', data['message'])
            self.assertIn('fail', data['status'])
