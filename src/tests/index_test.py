import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test"

from sqlalchemy import text  # pylint: disable=wrong-import-position

from config import app, db  # pylint: disable=wrong-import-position
from db_helper import reset_db, seed_db, setup_db  # pylint: disable=wrong-import-position
import index  # noqa: F401, pylint: disable=unused-import,wrong-import-position


class IndexRouteTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        setup_db()
        reset_db()
        self.client = app.test_client()

    def _seed_and_get_martin_id(self):
        seed_db()
        return db.session.execute(
            text("SELECT id FROM reference_items WHERE key = 'Martin08'")
        ).scalar()

    def tearDown(self):
        db.session.remove()
        self.ctx.pop()


class TestIndexRoutes(IndexRouteTestCase):
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

    def test_create_article_reference_valid(self):
        response = self.client.post(
            "/references/new",
            data={
                "reference_type": "article",
                "key": "Dijkstra68",
                "author": "Edsger W. Dijkstra",
                "title": "Go To Statement Considered Harmful",
                "year": "1968",
                "journal": "Communications of the ACM",
                "pages": "147-148",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"1 reference", response.data)
        self.assertIn(b'<span class="reference-type article">ARTICLE</span>', response.data)
        self.assertIn(b"<dt>Journal</dt><dd>Communications of the ACM</dd>", response.data)
        self.assertNotIn(b"<dt>Publisher</dt>", response.data)

        row = db.session.execute(
            text("SELECT * FROM reference_items WHERE key = 'Dijkstra68'")
        ).mappings().first()
        self.assertIsNotNone(row)
        self.assertEqual(row["author"], "Edsger W. Dijkstra")
        self.assertEqual(row["title"], "Go To Statement Considered Harmful")
        self.assertEqual(row["year"], 1968)
        self.assertEqual(row["journal"], "Communications of the ACM")
        self.assertEqual(row["pages"], "147-148")

        book_count = db.session.execute(
            text("SELECT COUNT(*) FROM reference_items WHERE ref_type = 'book'")
        ).scalar()
        self.assertEqual(book_count, 0)

    def test_create_article_reference_missing_required_field(self):
        response = self.client.post(
            "/references/new",
            data={
                "reference_type": "article",
                "key": "Dijkstra68",
                "author": "Edsger W. Dijkstra",
                "title": "Go To Statement Considered Harmful",
                "year": "1968",
                "journal": "",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"All required fields must be filled.", response.data)
        article_count = db.session.execute(
            text("SELECT COUNT(*) FROM reference_items WHERE ref_type = 'article'")
        ).scalar()
        self.assertEqual(article_count, 0)

    def test_create_reference_invalid_type(self):
        response = self.client.post(
            "/references/new",
            data={
                "reference_type": "invalid_type",
                "key": "Key1",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Choose a valid reference type.", response.data)

    def test_edit_article_reference_valid_updates_database(self):
        self.client.post(
            "/references/new",
            data={
                "reference_type": "article",
                "key": "Dijkstra68",
                "author": "Edsger W. Dijkstra",
                "title": "Go To Statement Considered Harmful",
                "year": "1968",
                "journal": "CACM",
                "pages": "147-148",
            },
        )
        ref_id = db.session.execute(
            text("SELECT id FROM reference_items WHERE key = 'Dijkstra68'")
        ).scalar()

        get_response = self.client.get(f"/references/article/{ref_id}/edit")
        self.assertEqual(get_response.status_code, 200)
        self.assertIn(b"Edit article reference", get_response.data)

        post_response = self.client.post(
            f"/references/article/{ref_id}/edit",
            data={
                "key": "Dijkstra68_v2",
                "author": "Edsger W. Dijkstra",
                "title": "Go To Statement Considered Harmful",
                "year": "1968",
                "journal": "Communications of the ACM",
                "pages": "147-148",
            },
            follow_redirects=True,
        )
        self.assertEqual(post_response.status_code, 200)
        self.assertIn(b"Dijkstra68_v2", post_response.data)
        self.assertIn(b"Communications of the ACM", post_response.data)

    def test_edit_reference_unknown_type_returns_404(self):
        response = self.client.get("/references/unknown/1/edit")
        self.assertEqual(response.status_code, 404)


class TestReferenceMutationRoutes(IndexRouteTestCase):
    def test_create_reference_year_beyond_sqlite_integer_limit_is_rejected(self):
        response = self.client.post(
            "/references/new",
            data={
                "key": "TooFar",
                "author": "Author",
                "title": "Title",
                "year": "9223372036854775808",
                "publisher": "Publisher",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Publication year is too large.", response.data)
        count = db.session.execute(
            text("SELECT COUNT(*) FROM reference_items")
        ).scalar()
        self.assertEqual(count, 0)

    def test_edit_reference_year_beyond_sqlite_integer_limit_is_rejected(self):
        ref_id = self._seed_and_get_martin_id()

        response = self.client.post(
            f"/references/book/{ref_id}/edit",
            data={
                "key": "Martin08",
                "author": "Robert C. Martin",
                "title": "Clean Code",
                "year": "9223372036854775808",
                "publisher": "Prentice Hall",
                "pages": "42",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Publication year is too large.", response.data)
        year = db.session.execute(
            text("SELECT year FROM reference_items WHERE id = :id"),
            {"id": ref_id},
        ).scalar()
        self.assertEqual(year, 2008)

    def test_delete_reference_removes_book_and_redirects(self):
        seed_db()
        ref_id = db.session.execute(
            text("SELECT id FROM reference_items WHERE key = 'Martin08'")
        ).scalar()

        response = self.client.post(
            f"/references/book/{ref_id}/delete",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Martin08", response.data)
        row = db.session.execute(
            text("SELECT * FROM reference_items WHERE id = :id"),
            {"id": ref_id},
        ).first()
        self.assertIsNone(row)

    def test_delete_reference_returns_404_for_unknown_type(self):
        response = self.client.post("/references/unknown/1/delete")
        self.assertEqual(response.status_code, 404)

    def test_delete_reference_returns_404_for_nonexistent_reference(self):
        response = self.client.post("/references/book/999/delete")
        self.assertEqual(response.status_code, 404)

    def test_delete_reference_shows_error_and_preserves_reference_on_database_failure(self):
        ref_id = self._seed_and_get_martin_id()
        db.session.execute(text("""
            CREATE TRIGGER prevent_book_reference_delete
            BEFORE DELETE ON reference_items
            BEGIN
                SELECT RAISE(ABORT, 'delete not allowed');
            END
        """))
        db.session.commit()

        try:
            response = self.client.post(
                f"/references/book/{ref_id}/delete",
                follow_redirects=True,
            )

            self.assertEqual(response.status_code, 500)
            self.assertIn(
                b"Could not delete the reference. Please try again.",
                response.data,
            )
            self.assertIn(b"Martin08", response.data)
            row = db.session.execute(
                text("SELECT * FROM reference_items WHERE id = :id"),
                {"id": ref_id},
            ).first()
            self.assertIsNotNone(row)
        finally:
            db.session.rollback()
            db.session.execute(text("DROP TRIGGER prevent_book_reference_delete"))
            db.session.commit()

    def test_delete_reference_shows_error_when_reference_list_cannot_load(self):
        db.session.execute(text("DROP TABLE reference_items"))
        db.session.commit()

        try:
            response = self.client.post("/references/inproceedings/1/delete")

            self.assertEqual(response.status_code, 500)
            self.assertIn(b"Could not delete the reference. Please try again.", response.data)
            self.assertIn(b"Could not load references.", response.data)
            self.assertNotIn(b"No references yet.", response.data)
        finally:
            setup_db()
