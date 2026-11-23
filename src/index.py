from os import getenv

from flask import abort, jsonify, redirect, render_template, request, url_for
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from config import app, db
from db_helper import reset_db, seed_db
from repositories.reference_repository import get_reference, update_reference

REFERENCE_FIELDS = {
    "book": ("key", "author", "title", "year", "publisher", "pages"),
    # "article": (),
    # "inproceedings": (),
}

REQUIRED_FIELDS = {
    "book": ("key", "author", "title", "year", "publisher"),
    # "article": (),
    # "inproceedings": (),
}


def read_reference_form(ref_type):
    fields = REFERENCE_FIELDS[ref_type]
    return {f: request.form.get(f, "").strip() for f in fields}


def validate_reference_form(ref_type, filled):
    required = REQUIRED_FIELDS[ref_type]
    if any(not filled[f] for f in required):
        return "All required fields must be filled."

    if not filled["year"].isdigit() or int(filled["year"]) <= 0:
        return "Publication year must be a positive number."

    return None


@app.get("/")
def index():
    result = db.session.execute(text("SELECT * FROM book_references"))
    references = result.fetchall()

    return render_template("index.html", references=references)


@app.route("/references/new", methods=["GET", "POST"])
def new_reference():
    if request.method == "GET":
        return render_template("new_reference.html", error=None, filled={})

    filled = read_reference_form("book")
    error = validate_reference_form("book", filled)
    if error:
        return render_template("new_reference.html", error=error, filled=filled), 400

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


@app.route("/references/<ref_type>/<int:ref_id>/edit", methods=["GET", "POST"])
def edit_reference(ref_type, ref_id):
    reference = get_reference(ref_type, ref_id)
    if reference is None:
        abort(404)

    if request.method == "GET":
        return render_template(
            "edit_reference.html",
            ref_type=ref_type,
            error=None,
            filled=reference,
        )

    filled = read_reference_form(ref_type)
    error = validate_reference_form(ref_type, filled)
    if error:
        return render_template(
            "edit_reference.html",
            ref_type=ref_type,
            error=error,
            filled=filled,
        ), 400

    try:
        update_reference(ref_type, ref_id, {**filled, "year": int(filled["year"])})
        return redirect(url_for("index"))
    except IntegrityError:
        db.session.rollback()
        return render_template(
            "edit_reference.html",
            ref_type=ref_type,
            error="Citation key already exists.",
            filled=filled,
        ), 400


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
