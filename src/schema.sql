CREATE TABLE IF NOT EXISTS book_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL CHECK (year > 0),
    publisher TEXT NOT NULL,
    pages TEXT
);

CREATE TABLE IF NOT EXISTS article_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER NOT NULL CHECK (year > 0),
    journal TEXT NOT NULL,
    pages TEXT
);
