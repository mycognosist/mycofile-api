# project/tests/test_user_model.py


from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError


# helper function to create test users more easily
def add_user(username, email, password):
    user = User(
        username=username,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return user


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('justatest', 'test@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        user = add_user('testing', 'testing@test.com', 'test')
        duplicate_user = User(
            username='testing',
            email='tester@test.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = add_user('anothertest', 'another@test.com', 'test')
        duplicate_user = User(
            username='justanothertest',
            email='another@test.com',
            password='test'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('justatest', 'test@test.com', 'test')
        user_two = add_user('justatest2', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
