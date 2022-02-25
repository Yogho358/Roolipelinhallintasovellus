
from werkzeug.security import check_password_hash, generate_password_hash


def register_user(db, username, password1, password2):
    if password1 != password2:
        raise Exception("Salasanat eivät ole samoja")

    if len(username) == 0:
        raise Exception("Täytyy antaa käyttäjätunnus")

    if len(password1) == 0:
        raise Exception("Täytyy antaa salasana")

    hash_value = generate_password_hash(password1)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    
        db.session.execute(sql, {"username": username,  "password": hash_value})
        db.session.commit()
    except Exception as e:
        raise Exception("Käyttäjänimi on jo olemassa")

def login_user(db, username, password):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        raise Exception(f"Käyttäjää {username} ei ole olemassa")
    hash_value = user.password
    if not check_password_hash(hash_value, password):
        raise Exception("Salasana on väärä")
    return user

def get_user(db, id):
    sql = "SELECT id, username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()


