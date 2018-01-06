# manage.py

import unittest
import coverage

from flask_script import Manager
from project import create_app, db
from project.api.models import Culture, Line
from project.tests.utils import add_culture
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
    add_culture('Pleurotus', 'ostreatus', 'K6', 'POK6001')
    add_culture('Hericium', 'erinaceus', 'JP', 'HEJP001')


@manager.command
def seed_line_db():
    """Seeds the Line table of the database."""
    l1 = Line(
        container='Petri',
        substrate='LME',
        culture_id='POK6001'
    )
    l2 = Line(
        container='Petri',
        substrate='LME',
        culture_id='POK6001'
    )
    l11 = Line(
        container='Petri',
        substrate='LME',
        culture_id='POK6001',
        parent=l1
    )
    l12 = Line(
        container='Petri',
        substrate='LME',
        culture_id='POK6001',
        parent=l1
    )
    l13 = Line(
        container='Petri',
        substrate='LME',
        culture_id='POK6001',
        parent=l1
    )
    l111 = Line(
        container='Jar (GM)',
        substrate='Wheat grain',
        culture_id='POK6001',
        parent=l11
    )
    l1111 = Line(
        container='Jar (1L)',
        substrate='Wheat grain',
        culture_id='POK6001',
        parent=l111
    )
    l11111 = Line(
        container='Bag',
        substrate='Hemp hurd',
        culture_id='POK6001',
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
