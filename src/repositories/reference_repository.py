from sqlalchemy import text

from config import db

REFERENCE_TYPES = ("book", "article", "inproceedings")


def get_references(folder_id=None):
    where = "WHERE folder_id = :folder_id" if folder_id is not None else ""
    sql = text(f"""
        SELECT *
        FROM reference_items
        {where}
        ORDER BY id
    """)

    rows = db.session.execute(sql, {"folder_id": folder_id}).mappings()
    return [dict(row) for row in rows]


def create_reference(ref_type, data, folder_id):
    if ref_type not in REFERENCE_TYPES:
        raise ValueError(f"Unknown reference type: {ref_type}")

    params = {
        "folder_id": folder_id,
        "ref_type": ref_type,

        # shared fields
        "key": data["key"],
        "title": data["title"],
        "author": data["author"],
        "year": data["year"],

        # type based
        "publisher": data.get("publisher"),
        "journal": data.get("journal"),
        "booktitle": data.get("booktitle"),
        "pages": data.get("pages", ""),
    }

    sql = text("""
        INSERT INTO reference_items (
            folder_id, ref_type, key, title, author,
            year, publisher, journal, booktitle, pages
        ) VALUES (
            :folder_id, :ref_type, :key, :title, :author,
            :year, :publisher, :journal, :booktitle, :pages
        )
    """)

    result = db.session.execute(sql, params)
    db.session.commit()

    return result.lastrowid


def get_reference(ref_type, ref_id):
    if ref_type not in REFERENCE_TYPES:
        return None

    sql = text("""
        SELECT *
        FROM reference_items
        WHERE id = :id
          AND ref_type = :ref_type
    """)

    row = db.session.execute(
        sql,
        {"id": ref_id, "ref_type": ref_type},
    ).mappings().first()

    return dict(row) if row is not None else None


def update_reference(ref_type, ref_id, data):
    if ref_type not in REFERENCE_TYPES:
        return False

    columns = ", ".join(f"{key} = :{key}" for key in data)
    sql = text(f"""
        UPDATE reference_items
        SET {columns}
        WHERE id = :id
          AND ref_type = :ref_type
    """)

    result = db.session.execute(
        sql,
        {**data, "id": ref_id, "ref_type": ref_type},
    )
    db.session.commit()

    return result.rowcount > 0


def remove_reference(ref_type, ref_id):
    if ref_type not in REFERENCE_TYPES:
        return False

    sql = text("""
        DELETE FROM reference_items
        WHERE id = :id
          AND ref_type = :ref_type
    """)

    result = db.session.execute(
        sql,
        {"id": ref_id, "ref_type": ref_type},
    )
    db.session.commit()

    return result.rowcount > 0
