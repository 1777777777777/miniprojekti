from sqlalchemy import text

from config import db

REFERENCE_TABLES = {
    "book": "book_references",
    "article": "article_references",
    # "inproceedings": "inproceedings_references",
}

REFERENCE_COLUMNS = {
    "book": {"key", "author", "title", "year", "publisher", "pages"},
    "article": {"key", "author", "title", "year", "journal", "pages"},
}



def get_reference(ref_type, ref_id):
    if ref_type not in REFERENCE_TABLES:
        return None

    table = REFERENCE_TABLES[ref_type]

    sql = text(f"SELECT * FROM {table} WHERE id = :id")
    row = db.session.execute(sql, {"id": ref_id}).mappings().first()

    if row is None:
        return None

    return dict(row)


def update_reference(ref_type, ref_id, data):
    if ref_type not in REFERENCE_TABLES:
        return False

    table = REFERENCE_TABLES[ref_type]
    columns = ", ".join(f"{key} = :{key}" for key in data)

    sql = text(f"UPDATE {table} SET {columns} WHERE id = :id")
    result = db.session.execute(sql, {**data, "id": ref_id})
    db.session.commit()

    return result.rowcount > 0
