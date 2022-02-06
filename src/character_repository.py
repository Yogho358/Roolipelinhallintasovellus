

def create_character(db, user_id, name, hp = 20):
    sql = "INSERT INTO characters (user_id, name, current_hp, max_hp) VALUES (:user_id, :name, :current_hp, :max_hp)"
    db.session.execute(sql, {"name": name, "user_id": user_id, "current_hp": hp, "max_hp": hp})
    db.session.commit()

def get_users_characters(db, user_id):
    sql = "SELECT * FROM characters WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    characters = result.fetchall()
    return characters

def get_character(db, id):
    sql = "SELECT * FROM characters WHERE id =:id"
    result = db.session.execute(sql, {"id":id})
    character = result.fetchone()
    return character