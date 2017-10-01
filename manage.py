# manage.py

import unittest, coverage

from flask_script import Manager
from project import create_app, db
from project.api.models import Culture, User
from flask_migrate import MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*'
    ]
)
COV.start()

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover(
        'project/tests',
        pattern='test*.py'
    )
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_culture_db():
    """Seeds the Culture table of the database."""
    db.session.add(Culture(
        genus='Pleurotus',
        species='ostreatus',
        strain='K6',
        unique_id='POK6001'
    ))
    db.session.add(Culture(
        genus='Hericium',
        species='erinaceus',
        strain='JP',
        unique_id='HEJP001'
    ))
    db.session.commit()


@manager.command
def seed_user_db():
    """Seeds the User table of the database."""
    db.session.add(User(
        username='mycognosist',
        email='gnomad@cryptolab.net'
    ))
    db.session.add(User(
        username='solar',
        email='solar@punk.earth'
    ))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
