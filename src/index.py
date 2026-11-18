from os import getenv

from flask import jsonify, redirect, render_template, request, url_for
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from config import app, db
from db_helper import reset_db, seed_db


@app.get("/")
def index():
    result = db.session.execute(text("SELECT * FROM book_references"))
    references = result.fetchall()

    return render_template("index.html", references=references)


@app.route("/references/new", methods=["GET", "POST"])
def new_reference():
    if request.method == "POST":
        fields = ("key", "author", "title", "year", "publisher", "pages")
        filled = {f: request.form.get(f, "").strip() for f in fields}

        if any(not filled[f] for f in ("key", "author", "title", "year", "publisher")):
            return render_template(
                "new_reference.html",
                error="All required fields must be filled.",
                filled=filled,
            ), 400

        if not filled["year"].isdigit() or int(filled["year"]) <= 0:
            return render_template(
                "new_reference.html",
                error="Publication year must be a positive number.",
                filled=filled,
            ), 400

        try:
            db.session.execute(
                text("""
                    INSERT INTO book_references
                        (key, author, title, year, publisher, pages)
                    VALUES
                        (:key, :author, :title, :year, :publisher, :pages)
                """),
                {**filled, "year": int(filled["year"])},
            )
            db.session.commit()
            return redirect(url_for("index"))
        except IntegrityError:
            db.session.rollback()
            return render_template(
                "new_reference.html",
                error="Citation key already exists.",
                filled=filled,
            ), 400

    return render_template("new_reference.html", error=None, filled={})


if getenv("TEST_ENV") == "true":
    @app.get("/seed_db")
    def seed_database():
        seed_db()
        return jsonify({"message": "db seeded"})

    @app.get("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)