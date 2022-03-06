def create_npc(db, template_name, name, hp, attack_skill, defence_skill, weapon_id, description):
    if len(template_name) == 0:
        raise Exception("Täytyy antaa nimi ei-pelaajahahmomallille")
    if not hp:
        hp = 20
    if not attack_skill:
        attack_skill = 50
    if not defence_skill:
        defence_skill = 50
    try:
        sql = "INSERT INTO npcs (template_name, name, current_hp, max_hp, attack_skill, defence_skill, weapon_id, description) VALUES (:template_name, :name, :hp, :hp, :attack_skill, :defence_skill, :weapon_id, :description)"
        db.session.execute(sql, {"template_name":template_name, "name":name, "hp":hp, "attack_skill":attack_skill, "defence_skill":defence_skill, "weapon_id":weapon_id, "description":description})
        db.session.commit()
    except:
        raise Exception(f"Malli nimeltä {template_name} on jo olemassa")

def add_npc_to_game(db, game_id, template_name, name, hp, attack_skill, defence_skill, weapon_id, description):
    if len(name) == 0:
        raise Exception("Täytyy antaa nimi")
    sql = "INSERT INTO npcs (template_name, name, current_hp, max_hp, attack_skill, defence_skill, weapon_id, description, game_id) VALUES (:template_name, :name, :hp, :hp, :attack_skill, :defence_skill, :weapon_id, :description, :game_id)"
    db.session.execute(sql, {"template_name":template_name, "name":name, "hp":hp, "attack_skill":attack_skill, "defence_skill":defence_skill, "weapon_id":weapon_id, "description":description, "game_id":game_id})
    db.session.commit()

def get_npc(db, id):
    sql = "SELECT id,template_name, name, current_hp, max_hp, attack_skill, defence_skill, weapon_id, description FROM npcs WHERE id=:id"
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

def get_npc_templates(db):
    sql = "SELECT * FROM npcs n WHERE game_id IS NULL ORDER BY name"
    result = db.session.execute(sql)
    return result.fetchall()

def delete_npc(db, id):
    sql = "DELETE FROM npcs WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()