def create_npc(db, name, hp, attack_skill, defence_skill, weapon_id, description):
    if len(name) == 0:
        raise Exception("Täytyy antaa nimi ei-pelaajahahmolle")
    if not hp:
        hp = 20
    if not attack_skill:
        attack_skill = 50
    if not defence_skill:
        defence_skill = 50
    sql = "INSERT INTO npcs (name, current_hp, max_hp, attack_skill, defence_skill, weapon_id, description) VALUES (:name, :hp, :hp, :attack_skill, :defence_skill, :weapon_id, :description)"
    db.session.execute(sql, {"name":name, "hp":hp, "attack_skill":attack_skill, "defence_skill":defence_skill, "weapon_id":weapon_id, "description":description})
    db.session.commit()

def get_npc(db, id):
    sql = "SELECT id, name, current_hp, max_hp, attack_skill, defence_skill, weapon_id, description FROM npcs WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def change_npc_health(db, id, amount, current, max, healing):
    if not healing:
        amount = 0 - amount
    if current + amount > max:
        amount = max - current
    sql = "UPDATE npcs SET current_hp=current_hp+:amount WHERE id=:id"
    db.session.execute(sql, {"amount": amount, "id":id})
    db.session.commit()

def modify_character(db, id, name, hp, attack_skill, defence_skill):
    sql = "UPDATE npcs SET name=:name, max_hp=:hp, attack_skill=:attack_skill, defence_skill=:defence_skill WHERE id=:id"
    db.session.execute(sql, {"name":name, "hp":hp, "attack_skill":attack_skill, "defence_skill":defence_skill, "id":id})
    db.session.commit()

def set_weapon(db, npc_id, weapon_id):
    sql = "UPDATE npcs SET weapon_id=:weapon_id WHERE id=:npc_id"
    db.session.execute(sql, {"weapon_id":weapon_id, "npc_id":npc_id})
    db.session.commit()