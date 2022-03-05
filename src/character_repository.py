

def create_character(db, user_id, name, hp = 20, weapon_id = 1):
    if len(name) == 0:
        raise Exception("Täytyy antaa nimi")
    sql = "INSERT INTO characters (user_id, name, current_hp, max_hp, attack_skill, defence_skill, weapon_id) VALUES (:user_id, :name, :current_hp, :max_hp, :attack_skill, :defence_skill, :weapon_id)"
    db.session.execute(sql, {"name": name, "user_id": user_id, "current_hp": hp, "max_hp": hp, "attack_skill":50, "defence_skill":50, "weapon_id": weapon_id})
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

def add_character_to_game(db, character_id, game_id):
    sql = "UPDATE characters SET game_id=:game_id WHERE id=:character_id"
    db.session.execute(sql, {"game_id":game_id, "character_id":character_id})
    db.session.commit()

def remove_character_from_game(db, character_id):
    sql = "UPDATE characters SET game_id=NULL WHERE id=:character_id"
    db.session.execute(sql, {"character_id":character_id})
    db.session.commit()

def set_weapon(db, character_id, weapon_id):
    sql = "UPDATE characters SET weapon_id=:weapon_id WHERE id=:character_id"
    db.session.execute(sql, {"weapon_id":weapon_id, "character_id":character_id})
    db.session.commit()

def mofify_character(db, character_id, name, hp, attack_skill, defence_skill):
    sql = "UPDATE characters SET name=:name, max_hp=:hp, attack_skill=:attack_skill, defence_skill=:defence_skill WHERE id=:character_id"
    db.session.execute(sql, {"name":name, "hp":hp, "attack_skill":attack_skill, "defence_skill":defence_skill, "character_id":character_id})
    db.session.commit()
