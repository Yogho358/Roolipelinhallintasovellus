def create_game(db, name, game_master_id):
    sql = "INSERT INTO games (name, game_master_id) VALUES (:name, :game_master_id)"
    db.session.execute(sql, {"name":name, "game_master_id":game_master_id})
    db.session.commit()

def get_mastered_games(db, id):
    sql = "SELECT * FROM games WHERE game_master_id=:id"
    result = db.session.execute(sql, {"id":id})
    games = result.fetchall()
    return games

def get_all_games(db):
    sql = "SELECT * FROM games"
    result = db.session.execute(sql)
    return result.fetchall()

def get_game(db, id):
    sql = "SELECT * FROM games WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def get_players_for_game(db, game_id):
    sql = "SELECT u.* FROM users u, playersingames p WHERE u.id = p.user_id AND p.game_id=:game_id"
    result = db.session.execute(sql, {"game_id":game_id})
    return result.fetchall()

def check_if_in_game(db, user_id, game_id):
    sql = "SELECT 1 FROM users u, playersingames p WHERE u.id = p.user_id AND p.game_id=:game_id AND p.user_id=:user_id"
    result = db.session.execute(sql, {"game_id":game_id, "user_id":user_id})
    if result.fetchone():
        return True
    return False

def add_player_to_game(db, user_id, game_id):

    if check_if_in_game(db, user_id, game_id):
        raise Exception("Pelaaja on jo pelissä")

    sql = "INSERT INTO playersingames (user_id, game_id) VALUES (:user_id, :game_id)"
    db.session.execute(sql, {"user_id":user_id, "game_id":game_id})
    db.session.commit()

def remove_player_from_game(db, user_id, game_id):
    sql = "DELETE FROM playersingames WHERE user_id=:user_id AND game_id=:game_id"
    db.session.execute(sql, {"user_id":user_id, "game_id":game_id})
    db.session.commit()

def get_weapons_available_for_game(db, game_id):
    sql = "SELECT * FROM weapons w WHERE NOT EXISTS(SELECT * FROM weaponsingames g WHERE w.id = g.weapon_id AND g.game_id = :game_id)"
    result = db.session.execute(sql, {"game_id":game_id})
    return result.fetchall()

def get_weapons_in_game(db, game_id):
    sql = "SELECT w.* FROM weapons w, weaponsingames g WHERE w.id = g.weapon_id AND g.game_id = :game_id"
    result = db.session.execute(sql, {"game_id":game_id})
    return result.fetchall()

def add_weapon_to_game(db, weapon_id, game_id):
    sql = "INSERT INTO weaponsingames (weapon_id, game_id) VALUES (:weapon_id, :game_id)"
    db.session.execute(sql, {"weapon_id":weapon_id, "game_id": game_id})
    db.session.commit()

def remove_weapon_from_game(db, weapon_id, game_id):
    sql = "DELETE FROM weaponsingames WHERE weapon_id=:weapon_id AND game_id=:game_id"
    db.session.execute(sql, {"weapon_id":weapon_id, "game_id":game_id})
    db.session.commit()