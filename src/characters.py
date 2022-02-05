def create_character(db, name):
    sql = "INSERT INTO characters (name) VALUES (:name)"
    db.session.execute(sql, {"name": name})
    db.session.commit()