import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

from sqlalchemy import text  # pylint: disable=wrong-import-position
from sqlalchemy.exc import IntegrityError  # pylint: disable=wrong-import-position

from config import app, db  # pylint: disable=wrong-import-position
from db_helper import reset_db, seed_db, setup_db  # pylint: disable=wrong-import-position
from repositories.folder_repository import (  # pylint: disable=wrong-import-position
    create_folder,
    get_or_create_default_folder,
)
from repositories.reference_repository import (  # pylint: disable=wrong-import-position
    create_reference,
    get_reference,
    get_references,
    remove_reference,
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
            text("SELECT id FROM reference_items WHERE key = :key"),
            {"key": key},
        ).scalar()

    def _insert_article(self, folder_id=None):
        target_folder_id = folder_id or get_or_create_default_folder()["id"]
        return create_reference(
            "article",
            {
                "key": "Dijkstra68",
                "title": "Go To Statement Considered Harmful",
                "author": "Edsger W. Dijkstra",
                "year": 1968,
                "journal": "CACM",
                "pages": "147-148",
            },
            target_folder_id,
        )

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

    def test_get_reference_returns_existing_article_reference(self):
        ref_id = self._insert_article()

        reference = get_reference("article", ref_id)

        self.assertIsNotNone(reference)
        self.assertEqual(reference["id"], ref_id)
        self.assertEqual(reference["key"], "Dijkstra68")
        self.assertEqual(reference["title"], "Go To Statement Considered Harmful")
        self.assertEqual(reference["author"], "Edsger W. Dijkstra")
        self.assertEqual(reference["year"], 1968)
        self.assertEqual(reference["journal"], "CACM")
        self.assertEqual(reference["pages"], "147-148")

    def test_update_reference_updates_existing_article_reference(self):
        ref_id = self._insert_article()
        updated_data = {
            "key": "Dijkstra68_v2",
            "title": "Go To Statement Considered Harmful (Revised)",
            "author": "E. W. Dijkstra",
            "year": 1969,
            "journal": "Communications of the ACM",
            "pages": "147-149",
        }

        updated = update_reference("article", ref_id, updated_data)
        reference = get_reference("article", ref_id)

        self.assertTrue(updated)
        self.assertEqual(reference["key"], "Dijkstra68_v2")
        self.assertEqual(reference["journal"], "Communications of the ACM")
        self.assertEqual(reference["year"], 1969)

    def test_remove_reference_deletes_existing_book_reference(self):
        ref_id = self._get_id_by_key("Martin08")

        deleted = remove_reference("book", ref_id)

        self.assertTrue(deleted)
        self.assertIsNone(get_reference("book", ref_id))

    def test_remove_reference_returns_false_for_nonexistent_id(self):
        self.assertFalse(remove_reference("book", 999))

    def test_remove_reference_returns_false_for_unknown_type(self):
        self.assertFalse(remove_reference("unknown", 1))

    def test_remove_reference_deletes_existing_article_reference(self):
        ref_id = self._insert_article()

        deleted = remove_reference("article", ref_id)

        self.assertTrue(deleted)
        self.assertIsNone(get_reference("article", ref_id))

    def test_get_references_filters_by_folder(self):
        other_folder = create_folder("Seminar")
        self._insert_article(folder_id=other_folder["id"])

        self.assertEqual(len(get_references()), 5)
        folder_refs = get_references(folder_id=other_folder["id"])
        self.assertEqual(len(folder_refs), 1)
        self.assertEqual(folder_refs[0]["key"], "Dijkstra68")
        self.assertEqual(folder_refs[0]["journal"], "CACM")

    def test_same_key_allowed_in_different_folders(self):
        other_folder = create_folder("Seminar")
        ref_id = create_reference(
            "book",
            {
                "key": "Martin08",
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "year": 2008,
                "publisher": "Prentice Hall",
            },
            other_folder["id"],
        )
        self.assertEqual(get_reference("book", ref_id)["folder_id"], other_folder["id"])

    def test_duplicate_key_rejected_within_same_folder(self):
        default_folder = get_or_create_default_folder()
        with self.assertRaises(IntegrityError):
            create_reference(
                "article",
                {
                    "key": "Martin08",
                    "title": "Duplicate",
                    "author": "Author",
                    "year": 2022,
                    "journal": "Journal",
                },
                default_folder["id"],
            )
        db.session.rollback()
