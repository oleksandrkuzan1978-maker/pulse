"""Regression checks using isolated SQLite databases; never the configured app DB."""
import unittest
from pathlib import Path

from flask_migrate import upgrade, downgrade, stamp
from app import create_app
from app.models import db

MIGRATIONS = str(Path(__file__).resolve().parents[1] / 'migrations')


class MigrationTests(unittest.TestCase):
    def setUp(self):
        class Config:
            TESTING = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        self.app = create_app(Config)
        self.context = self.app.app_context()
        self.context.push()

    def tearDown(self):
        db.session.remove()
        db.engine.dispose()
        self.context.pop()

    def run_upgrade(self, revision='head'):
        upgrade(directory=MIGRATIONS, revision=revision)

    def test_fresh_database_and_api(self):
        self.run_upgrade()
        category_id = db.session.execute(db.text(
            "SELECT id FROM categories WHERE name='General'"
        )).scalar_one()
        response = self.app.test_client().post('/questions', json={
            'text': 'Migration test', 'category_id': category_id,
        })
        self.assertEqual(response.status_code, 201)
        self.run_upgrade()
        self.assertEqual(db.session.execute(db.text(
            "SELECT count(*) FROM categories WHERE name='General'"
        )).scalar_one(), 1)

    def test_existing_questions_and_answers_survive(self):
        self.run_upgrade('f7f26ce384b9')
        db.session.execute(db.text("INSERT INTO questions(id,text) VALUES(7,'Existing')"))
        db.session.execute(db.text('INSERT INTO answers(id,question_id,is_agree) VALUES(8,7,1)'))
        db.session.commit()
        self.run_upgrade()
        row = db.session.execute(db.text(
            'SELECT q.text,c.name FROM questions q JOIN categories c ON c.id=q.category_id WHERE q.id=7'
        )).one()
        self.assertEqual(tuple(row), ('Existing', 'General'))
        self.assertEqual(db.session.execute(db.text('SELECT question_id FROM answers WHERE id=8')).scalar_one(), 7)
        self.assertEqual(db.session.execute(db.text('PRAGMA foreign_key_check')).all(), [])

    def test_previously_applied_category_revision(self):
        db.create_all()
        stamp(directory=MIGRATIONS, revision='e5fb1b66a99f')
        self.run_upgrade()
        self.assertEqual(db.session.execute(db.text('SELECT name FROM categories')).scalar_one(), 'General')
        downgrade(directory=MIGRATIONS, revision='e5fb1b66a99f')
        self.run_upgrade()
        self.assertEqual(db.session.execute(db.text('SELECT count(*) FROM categories')).scalar_one(), 1)

    def test_legacy_duplicate_revision(self):
        self.run_upgrade('f7f26ce384b9')
        # Simulate an old DB created by the equivalent d7ac53a809c1 root.
        stamp(directory=MIGRATIONS, revision='d7ac53a809c1')
        self.run_upgrade()
        self.assertEqual(db.session.execute(db.text('SELECT name FROM categories')).scalar_one(), 'General')

    def test_full_downgrade_and_reupgrade(self):
        self.run_upgrade()
        downgrade(directory=MIGRATIONS, revision='base')
        self.run_upgrade()
        self.assertEqual(db.session.execute(db.text('SELECT count(*) FROM categories')).scalar_one(), 1)


if __name__ == '__main__':
    unittest.main()
