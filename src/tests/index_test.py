import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

from sqlalchemy import text  # pylint: disable=wrong-import-position

from config import app, db  # pylint: disable=wrong-import-position
from db_helper import reset_db, seed_db, setup_db  # pylint: disable=wrong-import-position
import index  # noqa: F401, pylint: disable=unused-import,wrong-import-position


class TestIndexRoutes(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        setup_db()
        reset_db()
        self.client = app.test_client()

    def _seed_and_get_martin_id(self):
        seed_db()
        return db.session.execute(
            text("SELECT id FROM book_references WHERE key = 'Martin08'")
        ).scalar()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()

    def test_index_empty_db(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"0 references", response.data)
        self.assertIn(b"No references yet.", response.data)

    def test_index_seeded_db(self):
        seed_db()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"4 references", response.data)
        self.assertIn(b"Martin08", response.data)

    def test_new_reference_page(self):
        response = self.client.get("/references/new")
        self.assertEqual(response.status_code, 200)

    def test_create_reference_valid(self):
        response = self.client.post(
            "/references/new",
            data={
                "key": "Knuth97",
                "author": "Donald E. Knuth",
                "title": "The Art of Computer Programming",
                "year": "1997",
                "publisher": "Addison-Wesley",
                "pages": "1-10",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"1 reference", response.data)
        self.assertIn(b"Knuth97", response.data)

    def test_create_reference_missing_required_field(self):
        response = self.client.post(
            "/references/new",
            data={
                "key": "Knuth97",
                "author": "",
                "title": "TAOCP",
                "year": "1997",
                "publisher": "AW",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"All required fields must be filled.", response.data)

    def test_create_reference_invalid_year(self):
        response = self.client.post(
            "/references/new",
            data={
                "key": "Knuth97",
                "author": "Knuth",
                "title": "TAOCP",
                "year": "0",
                "publisher": "AW",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Publication year must be a positive number.", response.data)

    def test_create_reference_duplicate_key(self):
        seed_db()
        response = self.client.post(
            "/references/new",
            data={
                "key": "Martin08",
                "author": "A",
                "title": "B",
                "year": "2020",
                "publisher": "C",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Citation key already exists.", response.data)

    def test_edit_reference_page_prefills_existing_values(self):
        ref_id = self._seed_and_get_martin_id()

        response = self.client.get(f"/references/book/{ref_id}/edit")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit book reference", response.data)
        self.assertIn(b'value="Martin08"', response.data)
        self.assertIn(b'value="Robert C. Martin"', response.data)
        self.assertIn(b'value="2008"', response.data)

    def test_edit_reference_page_returns_404_for_nonexistent_reference(self):
        response = self.client.get("/references/book/999/edit")
        self.assertEqual(response.status_code, 404)

    def test_edit_reference_valid_updates_database(self):
        ref_id = self._seed_and_get_martin_id()

        response = self.client.post(
            f"/references/book/{ref_id}/edit",
            data={
                "key": "Martin08_v2",
                "author": "Robert C. Martin",
                "title": "Clean Code 2nd Edition",
                "year": "2009",
                "publisher": "Prentice Hall",
                "pages": "50",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Martin08_v2", response.data)
        self.assertIn(b"Clean Code 2nd Edition", response.data)

    def test_edit_reference_missing_field_preserves_user_input(self):
        ref_id = self._seed_and_get_martin_id()

        response = self.client.post(
            f"/references/book/{ref_id}/edit",
            data={
                "key": "EditedKey",
                "author": "",
                "title": "Edited Title",
                "year": "2015",
                "publisher": "Edited Publisher",
                "pages": "10",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"All required fields must be filled.", response.data)
        self.assertIn(b'value="EditedKey"', response.data)
        self.assertIn(b'value="Edited Title"', response.data)

    def test_edit_reference_duplicate_key_shows_error(self):
        ref_id = self._seed_and_get_martin_id()

        response = self.client.post(
            f"/references/book/{ref_id}/edit",
            data={
                "key": "Gamma94",
                "author": "Robert C. Martin",
                "title": "Clean Code",
                "year": "2008",
                "publisher": "Prentice Hall",
                "pages": "42",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Citation key already exists.", response.data)
        self.assertIn(b'value="Gamma94"', response.data)
