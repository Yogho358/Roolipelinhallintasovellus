

def create_character(db, user_id, name, hp = 20):
    sql = "INSERT INTO characters (user_id, name, current_hp, max_hp, attack_skill, defence_skill) VALUES (:user_id, :name, :current_hp, :max_hp, :attack_skill, :defence_skill)"
    db.session.execute(sql, {"name": name, "user_id": user_id, "current_hp": hp, "max_hp": hp, "attack_skill":50, "defence_skill":50})
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

def change_character_health(db, id, amount, current, max, healing):
    if not healing:
        amount = 0 - amount
    if current + amount > max:
        amount = max - current
    sql = "UPDATE characters SET current_hp=current_hp+:amount WHERE id=:id"
    db.session.execute(sql, {"amount": amount, "id":id})
    db.session.commit()