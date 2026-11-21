from sqlalchemy import text

from config import db

REFERENCE_TABLES = {
    "book": "book_references",
    # "article": "article_references",
    # "inproceedings": "inproceedings_references",
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
