CREATE TABLE IF NOT EXISTS folders (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT    UNIQUE NOT NULL CHECK (length(trim(name)) > 0)
);

CREATE TABLE IF NOT EXISTS reference_items (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    folder_id INTEGER NOT NULL REFERENCES folders(id) ON DELETE CASCADE,
    ref_type  TEXT    NOT NULL CHECK (ref_type IN ('book', 'article', 'inproceedings')),

    -- shared fields
    key       TEXT    NOT NULL,
    title     TEXT    NOT NULL,
    author    TEXT    NOT NULL,
    year      INTEGER NOT NULL CHECK (year > 0),

    -- type based
    publisher TEXT,
    journal   TEXT,
    booktitle TEXT,
    pages     TEXT,

    UNIQUE (folder_id, key)
);