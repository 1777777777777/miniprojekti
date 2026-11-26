import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

from sqlalchemy.exc import IntegrityError  # pylint: disable=wrong-import-position

from config import app, db  # pylint: disable=wrong-import-position
from db_helper import reset_db, setup_db  # pylint: disable=wrong-import-position
from repositories.folder_repository import (  # pylint: disable=wrong-import-position
    DEFAULT_FOLDER_NAME,
    create_folder,
    delete_folder,
    get_folder,
    get_folders,
    get_or_create_default_folder,
    rename_folder,
)
from repositories.reference_repository import (  # pylint: disable=wrong-import-position
    create_reference,
    get_references,
)


class TestFolderRepository(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.addCleanup(self._cleanup_context)
        setup_db()
        reset_db()

    def _cleanup_context(self):
        db.session.remove()
        self.app_context.pop()

    def test_create_and_get_folder(self):
        folder = create_folder("  Thesis  ")
        self.assertEqual(folder["name"], "Thesis")
        self.assertEqual(get_folder(folder["id"]), folder)

    def test_create_folder_rejects_duplicate_and_blank_name(self):
        create_folder("Thesis")
        with self.assertRaises(IntegrityError):
            create_folder("Thesis")
        db.session.rollback()

        with self.assertRaises(IntegrityError):
            create_folder("   ")
        db.session.rollback()

    def test_get_folders_returns_counts_newest_first(self):
        thesis = create_folder("Thesis")
        seminar = create_folder("Seminar")
        create_reference(
            "book",
            {
                "key": "Knuth97",
                "title": "The Art of Computer Programming",
                "author": "Donald E. Knuth",
                "year": 1997,
                "publisher": "Addison-Wesley",
            },
            thesis["id"],
        )

        self.assertEqual(
            get_folders(),
            [
                {"id": seminar["id"], "name": "Seminar", "reference_count": 0},
                {"id": thesis["id"], "name": "Thesis", "reference_count": 1},
            ],
        )

    def test_rename_folder(self):
        folder = create_folder("Draft")
        self.assertTrue(rename_folder(folder["id"], "Final"))
        self.assertEqual(get_folder(folder["id"])["name"], "Final")
        self.assertFalse(rename_folder(999, "Missing"))

    def test_delete_folder_cascades_references(self):
        folder_a = create_folder("Paper A")
        folder_b = create_folder("Paper B")
        create_reference(
            "inproceedings",
            {
                "key": "VPL11",
                "title": "Extreme Apprenticeship",
                "author": "Vihavainen",
                "year": 2011,
                "booktitle": "SIGCSE '11",
            },
            folder_a["id"],
        )
        create_reference(
            "article",
            {
                "key": "RefB",
                "title": "Paper B Ref",
                "author": "Author B",
                "year": 2021,
                "journal": "Journal B",
            },
            folder_b["id"],
        )

        self.assertTrue(delete_folder(folder_a["id"]))
        self.assertEqual(get_references(folder_a["id"]), [])
        self.assertEqual(len(get_references(folder_b["id"])), 1)
        self.assertFalse(delete_folder(999))

    def test_get_or_create_default_folder_is_idempotent(self):
        first = get_or_create_default_folder()
        second = get_or_create_default_folder()
        self.assertEqual(first["name"], DEFAULT_FOLDER_NAME)
        self.assertEqual(first, second)
