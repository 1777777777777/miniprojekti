from os import getenv

from flask import abort, jsonify, redirect, render_template, request, url_for
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from config import app, db
from db_helper import reset_db, seed_db
from repositories.folder_repository import get_or_create_default_folder
from repositories.reference_repository import (
    create_reference,
    get_reference,
    get_references,
    remove_reference,
    update_reference,
)

REFERENCE_FIELDS = {
    "book": ("key", "author", "title", "year", "publisher", "pages"),
    "article": ("key", "author", "title", "year", "journal", "pages"),
    "inproceedings": ("key", "author", "title", "year", "booktitle", "pages"),
}

REQUIRED_FIELDS = {
    "book": ("key", "author", "title", "year", "publisher"),
    "article": ("key", "author", "title", "year", "journal"),
    "inproceedings": ("key", "author", "title", "year", "booktitle"),
}

SQLITE_MAX_INTEGER = "9223372036854775807"


def read_reference_form(ref_type):
    fields = REFERENCE_FIELDS[ref_type]
    return {f: request.form.get(f, "").strip() for f in fields}


def validate_reference_form(ref_type, filled):
    required = REQUIRED_FIELDS[ref_type]
    if any(not filled[f] for f in required):
        return "All required fields must be filled."

    year = filled["year"]
    if not year.isascii() or not year.isdecimal():
        return "Publication year must be a positive number."

    normalized_year = year.lstrip("0")
    if not normalized_year:
        return "Publication year must be a positive number."

    if len(normalized_year) > len(SQLITE_MAX_INTEGER) or (
        len(normalized_year) == len(SQLITE_MAX_INTEGER)
        and normalized_year > SQLITE_MAX_INTEGER
    ):
        return "Publication year is too large."

    filled["year"] = normalized_year
    return None


@app.get("/")
def index():
    return render_template(
        "index.html",
        references=get_references(),
        error=None,
    )


@app.route("/references/new", methods=["GET", "POST"])
def new_reference():
    if request.method == "GET":
        return render_template(
            "new_reference.html",
            error=None,
            filled={"reference_type": "book"},
        )

    ref_type = request.form.get("reference_type", "book")
    filled = request.form.to_dict()
    filled["reference_type"] = ref_type

    if ref_type not in REFERENCE_FIELDS:
        return render_template(
            "new_reference.html",
            error="Choose a valid reference type.",
            filled=filled,
        ), 400

    filled.update(read_reference_form(ref_type))
    error = validate_reference_form(ref_type, filled)

    if error:
        return render_template(
            "new_reference.html",
            error=error,
            filled=filled,
        ), 400

    try:
        folder = get_or_create_default_folder()
        create_reference(ref_type, {**filled, "year": int(filled["year"])}, folder["id"])
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
    if ref_type not in REFERENCE_FIELDS:
        abort(404)

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


@app.post("/references/<ref_type>/<int:ref_id>/delete")
def delete_reference(ref_type, ref_id):
    try:
        deleted = remove_reference(ref_type, ref_id)
    except SQLAlchemyError:
        app.logger.exception("Could not delete reference %s/%s", ref_type, ref_id)
        db.session.rollback()
        try:
            references = get_references()
        except SQLAlchemyError:
            db.session.rollback()
            references = None

        return render_template(
            "index.html",
            references=references,
            error="Could not delete the reference. Please try again.",
        ), 500

    if not deleted:
        abort(404)

    return redirect(url_for("index"))


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
