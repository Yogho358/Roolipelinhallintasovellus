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
    sql = "SELECT u.id, u.username FROM users u, playersingames p WHERE u.id = p.user_id AND p.game_id=:game_id"
    result = db.session.execute(sql, {"game_id":game_id})
    return result.fetchall()