import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

from sqlalchemy import text  # pylint: disable=wrong-import-position

from config import app, db  # pylint: disable=wrong-import-position
from db_helper import reset_db, seed_db, setup_db  # pylint: disable=wrong-import-position
from repositories.reference_repository import get_reference  # pylint: disable=wrong-import-position


class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        setup_db()
        reset_db()
        seed_db()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def test_get_reference_returns_existing_book_reference(self):
        ref_id = db.session.execute(
            text("SELECT id FROM book_references WHERE key = 'Martin08'")
        ).scalar()

        reference = get_reference("book", ref_id)

        self.assertIsNotNone(reference)
        self.assertEqual(reference["id"], ref_id)
        self.assertEqual(reference["key"], "Martin08")
        self.assertEqual(
            reference["title"],
            "Clean Code: A Handbook of Agile Software Craftsmanship",
        )
        self.assertEqual(reference["author"], "Robert C. Martin")
        self.assertEqual(reference["year"], 2008)
        self.assertEqual(reference["publisher"], "Prentice Hall")
        self.assertEqual(reference["pages"], "42")

    def test_get_reference_returns_none_for_nonexistent_id(self):
        self.assertIsNone(get_reference("book", 999))

    def test_get_reference_returns_none_for_unknown_type(self):
        self.assertIsNone(get_reference("unknown", 1))
