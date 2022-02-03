
import unittest
from flask import Flask
from db import get_db
from users import register_user


app = Flask(__name__)
db = get_db(app)

def drop_tables():
    db.session.execute("DROP TABLE IF EXISTS test;")
    db.session.execute("DROP TABLE IF EXISTS users;")

class TestStuff(unittest.TestCase):
    

    def setUp(self): 
        
        db.session.execute("DROP TABLE IF EXISTS test;")
        db.session.execute("DROP TABLE IF EXISTS users;")
        db.session.execute("CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);")
        db.session.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);")

    def test_db_testing(self):
        db.session.execute("INSERT INTO test (txt) VALUES ('testi');")
        result = db.session.execute("SELECT * FROM test;")
        res = result.fetchall()
        drop_tables()
        self.assertEqual(res[0].txt, "testi")

    def test_should_save_user_to_db_on_registration(self):  
        register_user(db,"testman", "password")
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        drop_tables()
        self.assertEqual(len(users), 1)

    def test_should_save_users_with_right_name_on_registration(self):
        register_user(db, "testman", "password")
        register_user(db, "tester", "pass2")
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        drop_tables()
        self.assertEqual(users[1].username, "tester")


        


