def create_weapon(db, name, min_damage, max_damage, attack_modifier, defence_modifier, size, description):
    sql = "INSERT INTO weapons (name, min_damage, max_damage, attack_modifier, defence_modifier, size, description) VALUES (:name, :min_damage, :max_damage, :attack_modifier, :defence_modifier, :size, :description)"
    db.session.execute(sql, {"name":name, "min_damage":min_damage, "max_damage":max_damage, "attack_modifier":attack_modifier, "defence_modifier":defence_modifier, "size":size, "description":description})
    db.session.commit()

