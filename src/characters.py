def create_character(db, user_id, name):
    sql = "INSERT INTO characters (user_id, name) VALUES (:user_id, :name)"
    db.session.execute(sql, {"name": name, "user_id": user_id})
    db.session.commit()

def get_users_characters(db, user_id):
    sql = "SELECT * FROM characters WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    characters = result.fetchall()
    return characters