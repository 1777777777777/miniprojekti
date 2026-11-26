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

    def test_setup_db_creates_folders_table(self):
        self.assertIn("folders", tables())

    def test_setup_db_creates_reference_items_table(self):
        self.assertIn("reference_items", tables())

    def test_seed_db_inserts_example_references(self):
        seed_db()
        count = db.session.execute(
            text("SELECT COUNT(*) FROM reference_items")
        ).scalar()
        self.assertEqual(count, 4)

    def test_seed_db_is_idempotent(self):
        seed_db()
        seed_db()
        count = db.session.execute(
            text("SELECT COUNT(*) FROM reference_items")
        ).scalar()
        self.assertEqual(count, 4)

    def test_reset_db_clears_references_and_folders(self):
        seed_db()
        reset_db()
        ref_count = db.session.execute(
            text("SELECT COUNT(*) FROM reference_items")
        ).scalar()
        folder_count = db.session.execute(
            text("SELECT COUNT(*) FROM folders")
        ).scalar()
        self.assertEqual(ref_count, 0)
        self.assertEqual(folder_count, 0)
