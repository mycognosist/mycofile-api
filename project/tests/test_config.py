# project/tests/test_config.py


import os
import unittest

from flask import current_app
from flask_testing import TestCase
from project.config import basedir

from project import create_app

app = create_app()


class TestDevelopmentConfig(TestCase):
    """Ensure the app development configuration is correct."""
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(
            app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'sqlite:///' + os.path.join(basedir, 'app.db')
        )
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 30)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 0)


class TestTestingConfig(TestCase):
    """Ensure the app testing configuration is correct."""
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(
            app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'sqlite:///' + os.path.join(basedir, 'test.db')
        )
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 3)


class TestProductionConfig(TestCase):
    """Ensure the app production configuration is correct."""
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(
            app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 13)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 30)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 0)


if __name__ == '__main__':
    unittest.main()
