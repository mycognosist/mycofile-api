# project/tests/test_users.py

import json

from project.tests.base import BaseTestCase
from project import db
from project.api.models import User
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        user = add_user('justatest', 'test@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)
        self.assertTrue(user.admin == False)

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/users',
                data=json.dumps(dict()),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object does not have a username key."""
        add_user('mycognosist', 'gnomad@cryptolab.net', 'test')
        # update user
        user = User.query.filter_by(email='gnomad@cryptolab.net').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='gnomad@cryptolab.net',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/users',
                data=json.dumps(dict(
                    email='crash@cryptolab.net',
                    password='test'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        add_user('mycognosist', 'gnomad@cryptolab.net', 'test')
        # update user
        user = User.query.filter_by(email='gnomad@cryptolab.net').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='gnomad@cryptolab.net',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/users',
                data=json.dumps(dict(
                    username='mycognosist',
                    email='gnomad@cryptolab.net',
                    password='test'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """Ensure error is thrown if the JSON object does not have a password key."""
        add_user('test', 'test@test.com', 'test')
        # update user
        user = User.query.filter_by(email='test@test.com').first()
        user.admin = True
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/users',
                data=json.dumps(dict(
                    username='luna',
                    email='lunar@punk.system'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_not_admin(self):
        """Ensure error is thrown if non-admin tries to add user."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            # user login
            resp_login = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/api/v1/users',
                data=json.dumps(dict(
                    username='joel',
                    email='joel@joel.com',
                    password='test'
                )),
                content_type='application/json',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'You do not have permission to do that.')
            self.assertEqual(response.status_code, 401)

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('mycognosist', 'gnomad@cryptolab.net', 'test')
        with self.client:
            response = self.client.get(f'/api/v1/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('mycognosist', data['data']['username'])
            self.assertIn('gnomad@cryptolab.net', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/api/v1/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/api/v1/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('mycognosist', 'gnomad@cryptolab.net', 'password')
        add_user('solar', 'solar@punk.earth', 'password')
        with self.client:
            response=  self.client.get('/api/v1/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn(
                'mycognosist',
                data['data']['users'][0]['username']
            )
            self.assertIn(
                'gnomad@cryptolab.net',
                data['data']['users'][0]['email']
            )
            self.assertIn('solar', data['data']['users'][1]['username'])
            self.assertIn(
                'solar@punk.earth',
                data['data']['users'][1]['email']
            )
            self.assertIn('success', data['status'])
