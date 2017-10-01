# project/tests/test_user_model.py


from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = User(
            username='justatest',
            email='test@test.com',
            password='test',
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        user = User(
            username='testing',
            email='testing@test.com',
            password='test',
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='testing',
            email='tester@test.com',
            password='test',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = User(
            username='anothertest',
            email='another@test.com',
            password='test',
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='justanothertest',
            email='another@test.com',
            password='test',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = User(
            username='justatest',
            email='test@test.com',
            password='test',
        )
        db.session.add(user_one)
        db.session.commit()
        user_two = User(
            username='justatest2',
            email='test@test2.com',
            password='test',
        )
        db.session.add(user_two)
        db.session.commit()
        self.assertNotEqual(user_one.password, user_two.password)
