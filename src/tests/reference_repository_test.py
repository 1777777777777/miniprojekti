import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

from sqlalchemy import text  # pylint: disable=wrong-import-position
from sqlalchemy.exc import IntegrityError  # pylint: disable=wrong-import-position

from config import app, db  # pylint: disable=wrong-import-position
from db_helper import reset_db, seed_db, setup_db  # pylint: disable=wrong-import-position
from repositories.reference_repository import (  # pylint: disable=wrong-import-position
    get_reference,
    update_reference,
)


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

    def _get_id_by_key(self, key):
        return db.session.execute(
            text("SELECT id FROM book_references WHERE key = :key"),
            {"key": key},
        ).scalar()

    def test_get_reference_returns_existing_book_reference(self):
        ref_id = self._get_id_by_key("Martin08")

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

    def test_update_reference_updates_existing_book_reference(self):
        ref_id = self._get_id_by_key("Martin08")
        updated_data = {
            "key": "Martin08_edited",
            "title": "Clean Code (2nd ed.)",
            "author": "Robert Martin",
            "year": 2009,
            "publisher": "Pearson",
            "pages": "100-120",
        }

        updated = update_reference("book", ref_id, updated_data)
        reference = get_reference("book", ref_id)

        self.assertTrue(updated)
        self.assertEqual(reference["key"], "Martin08_edited")
        self.assertEqual(reference["title"], "Clean Code (2nd ed.)")
        self.assertEqual(reference["author"], "Robert Martin")
        self.assertEqual(reference["year"], 2009)
        self.assertEqual(reference["publisher"], "Pearson")
        self.assertEqual(reference["pages"], "100-120")

    def test_update_reference_returns_false_for_nonexistent_id(self):
        updated = update_reference(
            "book",
            999,
            {
                "key": "NewKey",
                "title": "Title",
                "author": "Author",
                "year": 2020,
                "publisher": "Publisher",
                "pages": "",
            },
        )
        self.assertFalse(updated)

    def test_update_reference_returns_false_for_unknown_type(self):
        self.assertFalse(update_reference("unknown", 1, {"title": "New"}))

    def test_update_reference_raises_integrity_error_on_duplicate_key(self):
        ref_id = self._get_id_by_key("Martin08")

        with self.assertRaises(IntegrityError):
            update_reference(
                "book",
                ref_id,
                {
                    "key": "Gamma94",
                    "title": "Clean Code",
                    "author": "Robert C. Martin",
                    "year": 2008,
                    "publisher": "Prentice Hall",
                    "pages": "42",
                },
            )
