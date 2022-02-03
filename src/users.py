from werkzeug.security import check_password_hash, generate_password_hash

def register_user(db, username, password):
    hash_value = generate_password_hash(password)   
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    
    db.session.execute(sql, {"username": username,  "password": hash_value})
    db.session.commit()
