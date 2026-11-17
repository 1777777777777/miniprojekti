from os import getenv
from flask import jsonify, render_template

from config import app, db
from db_helper import reset_db, seed_db
from sqlalchemy import text


@app.get("/")
def index():
    result = db.session.execute(text("SELECT * FROM book_references"))
    references = result.fetchall()

    return render_template("index.html", references=references)


@app.get("/references/new")
def new_reference():
    return render_template("new_reference.html")


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