def create_weapon(db, name, min_damage, max_damage, attack_modifier, defence_modifier, size, description):
    if len(name) == 0:
        raise Exception("Täytyy antaa nimi")
    if not min_damage:
        min_damage = 0
    if not max_damage:
        max_damage = 0
    if not attack_modifier:
        attack_modifier = 0
    if not defence_modifier:
        defence_modifier = 0
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
    res = result.fetchone()
    weapon_id = res[0]
    return weapon_id

def get_all_weapons(db):
    sql = "SELECT * FROM weapons ORDER BY name"
    result = db.session.execute(sql)
    return result.fetchall()