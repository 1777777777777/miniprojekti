import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

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
