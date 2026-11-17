import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

from sqlalchemy import text  # pylint: disable=wrong-import-position

from config import app, db  # pylint: disable=wrong-import-position
from db_helper import reset_db, seed_db, setup_db, tables  # pylint: disable=wrong-import-position


class TestDbHelper(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        setup_db()
        reset_db()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def test_setup_db_creates_book_references_table(self):
        self.assertIn("book_references", tables())

    def test_seed_db_inserts_example_references(self):
        seed_db()
        count = db.session.execute(
            text("SELECT COUNT(*) FROM book_references")
        ).scalar()
        self.assertEqual(count, 4)

    def test_seed_db_is_idempotent(self):
        seed_db()
        seed_db()
        count = db.session.execute(
            text("SELECT COUNT(*) FROM book_references")
        ).scalar()
        self.assertEqual(count, 4)

    def test_reset_db_clears_references(self):
        seed_db()
        reset_db()
        count = db.session.execute(
            text("SELECT COUNT(*) FROM book_references")
        ).scalar()
        self.assertEqual(count, 0)
