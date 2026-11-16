from flask import render_template

from config import app, db
from sqlalchemy import text

@app.get("/")
def index():
    result = db.session.execute(text("SELECT * FROM book_references"))
    references = result.fetchall()

    return render_template("index.html", references=references)


@app.get("/references/new")
def new_reference():
    return render_template("new_reference.html")


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)