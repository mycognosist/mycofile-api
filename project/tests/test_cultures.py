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
