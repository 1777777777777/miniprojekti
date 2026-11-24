import os

from sqlalchemy import text

from config import app, db


def tables():
    """Returns all table names from the database"""
    sql = text(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
    )

    result = db.session.execute(sql)
    return [row[0] for row in result.fetchall()]


def reset_db():
    """Clears all reference rows from the database."""
    print("Clearing reference tables")
    db.session.execute(text("DELETE FROM book_references"))
    db.session.execute(text("DELETE FROM article_references"))
    db.session.commit()


def setup_db():
    """
    Creates the database tables defined in schema.sql.
    Existing tables and their data are preserved.
    """
    print("Creating database")
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read().strip()

    if not schema_sql:
        return

    # Suoritetaan lauseet erikseen; SQLAlchemyn execute ei yleensä
    # suorita useita SQL-lauseita yhdellä kutsulla.
    for statement in schema_sql.split(";"):
        statement = statement.strip()
        if statement:
            db.session.execute(text(statement))

    db.session.commit()


def seed_db():
    """Inserts example references if the book_references table is empty."""
    result = db.session.execute(
        text("SELECT COUNT(*) FROM book_references")
    )
    count = result.scalar()

    if count == 0:
        db.session.execute(text("""
            INSERT INTO book_references
            (key, title, author, year, publisher, pages)
            VALUES
                (:key, :title, :author, :year, :publisher, :pages)
        """), [
            {
                "key": "Martin08",
                "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                "author": "Robert C. Martin",
                "year": 2008,
                "publisher": "Prentice Hall",
                "pages": "42",
            },
            {
                "key": "Gamma94",
                "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
                "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
                "year": 1994,
                "publisher": "Addison-Wesley Professional",
                "pages": "",
            },
            {
                "key": "Fowler99",
                "title": "Refactoring: Improving the Design of Existing Code",
                "author": "Martin Fowler",
                "year": 1999,
                "publisher": "Addison-Wesley Professional",
                "pages": "42–48",
            },
            {
                "key": "Thomas19",
                "title": "The Pragmatic Programmer",
                "author": "David Thomas and Andrew Hunt",
                "year": 2019,
                "publisher": "Addison-Wesley Professional",
                "pages": "",
            },
        ])
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        setup_db()