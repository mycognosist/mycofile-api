# manage.py

import unittest
import coverage

from flask_script import Manager
from project import create_app, db
from project.api.models import Culture, User, Line
from project.tests.utils import add_culture, add_user
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
    add_culture('Pleurotus', 'ostreatus', 'K6', 'POK6001', 1)
    add_culture('Hericium', 'erinaceus', 'JP', 'HEJP001', 2)


@manager.command
def seed_user_db():
    """Seeds the User table of the database."""
    add_user('mycognosist', 'gnomad@cryptolab.net', 'test')
    add_user('solar', 'solar@punk.earth', 'password')


@manager.command
def seed_line_db():
    """Seeds the Line table of the database."""
    l1 = Line(
        container='Petri',
        dimensions='65mm',
        substrate='LME',
        treatment='Sterilized',
        culture_id='POK6001',
        user_id=1,
        active=False
    )
    l2 = Line(
        container='Petri',
        dimensions='65mm',
        substrate='LME',
        treatment='Sterilized',
        culture_id='POK6001',
        user_id=1
    )
    l11 = Line(
        container='Petri',
        dimensions='65mm',
        substrate='LME',
        treatment='Sterilized',
        culture_id='POK6001',
        user_id=1,
        active=False,
        parent=l1
    )
    l12 = Line(
        container='Petri',
        dimensions='125mm',
        substrate='LME',
        treatment='Sterilized',
        culture_id='POK6001',
        user_id=1,
        contam=True,
        parent=l1
    )
    l13 = Line(
        container='Petri',
        dimensions='125mm',
        substrate='LME',
        treatment='Sterilized',
        culture_id='POK6001',
        user_id=1,
        backup=True,
        parent=l1
    )
    l111 = Line(
        container='Jar (GM)',
        dimensions='0.5L',
        substrate='Wheat grain',
        treatment='Sterilized',
        culture_id='POK6001',
        user_id=1,
        active=False,
        parent=l11
    )
    l1111 = Line(
        container='Jar',
        dimensions='1L',
        substrate='Wheat grain',
        treatment='Sterilized',
        culture_id='POK6001',
        user_id=1,
        active=False,
        parent=l111
    )
    l11111 = Line(
        container='Bag',
        dimensions='300mm x 1000mm',
        substrate='Hemp hurd',
        treatment='Pasteurized',
        culture_id='POK6001',
        user_id=1,
        parent=l1111
    )
    for line in [l1, l2, l11, l12, l13, l111, l1111, l11111]:
        line.save()


@manager.command
def print_lines():
    for line in Line.query.order_by(Line.path):
        print('{}{}: {}'.format(
            ' ' * line.level(),
            line.container,
            line.substrate,
            line.culture_id
        ))


if __name__ == '__main__':
    manager.run()
