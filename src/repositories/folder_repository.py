from sqlalchemy import text

from config import db

DEFAULT_FOLDER_NAME = "My refs"


def get_folders():
    sql = text("""
        SELECT f.id, f.name, COUNT(r.id) AS reference_count
        FROM folders f
        LEFT JOIN reference_items r ON r.folder_id = f.id
        GROUP BY f.id, f.name
        ORDER BY f.id DESC
    """)
    rows = db.session.execute(sql).mappings().all()
    return [dict(row) for row in rows]


def get_folder(folder_id):
    sql = text("SELECT id, name FROM folders WHERE id = :id")
    row = db.session.execute(sql, {"id": folder_id}).mappings().first()
    return dict(row) if row is not None else None


def create_folder(name):
    clean_name = name.strip()
    sql = text("INSERT INTO folders (name) VALUES (:name)")
    result = db.session.execute(sql, {"name": clean_name})
    db.session.commit()
    return {"id": result.lastrowid, "name": clean_name}


def rename_folder(folder_id, new_name):
    clean_name = new_name.strip()
    sql = text("UPDATE folders SET name = :name WHERE id = :id")
    result = db.session.execute(sql, {"name": clean_name, "id": folder_id})
    db.session.commit()
    return result.rowcount > 0


def delete_folder(folder_id):
    sql = text("DELETE FROM folders WHERE id = :id")
    result = db.session.execute(sql, {"id": folder_id})
    db.session.commit()
    return result.rowcount > 0


def get_or_create_default_folder():
    sql = text("SELECT id, name FROM folders WHERE name = :name")
    row = db.session.execute(sql, {"name": DEFAULT_FOLDER_NAME}).mappings().first()
    if row is not None:
        return dict(row)
    return create_folder(DEFAULT_FOLDER_NAME)
