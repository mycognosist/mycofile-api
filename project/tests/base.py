# project/tests/base.py

import os

from flask_testing import TestCase
from ..config import basedir
from project import app, db


class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('project.config')
        return app

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()


