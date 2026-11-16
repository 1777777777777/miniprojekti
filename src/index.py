from flask import render_template

from config import app


EXAMPLE_REFERENCES = [
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
]


@app.get("/")
def index():
    return render_template("index.html", references=EXAMPLE_REFERENCES)


@app.get("/references/new")
def new_reference():
    return render_template("new_reference.html")


if __name__ == "__main__":
    app.run(port=5001, host="0.0.0.0", debug=True)
