def create_weapon(db, name, min_damage, max_damage, attack_modifier, defence_modifier, size, description):
    sql = "INSERT INTO weapons (name, min_damage, max_damage, attack_modifier, defence_modifier, size, description) VALUES (:name, :min_damage, :max_damage, :attack_modifier, :defence_modifier, :size, :description)"
    db.session.execute(sql, {"name":name, "min_damage":min_damage, "max_damage":max_damage, "attack_modifier":attack_modifier, "defence_modifier":defence_modifier, "size":size, "description":description})
    db.session.commit()

def get_weapon(db, id):
    sql = "SELECT * FROM weapons WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_default_weapon_id(db):
    sql = "SELECT id FROM weapons WHERE name='Nyrkki'"
    result = db.session.execute(sql)
    weapon_id = result.fetchone()[0]
    return weapon_id