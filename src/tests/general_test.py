
import unittest
from flask import Flask
from db import get_db
from users import register_user, login_user


app = Flask(__name__)
db = get_db(app)

def register_testman():
        register_user(db, "testman", "password", "password")

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
        register_testman()
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        drop_tables()
        self.assertEqual(len(users), 1)

    def test_should_save_users_with_right_name_on_registration(self):
        register_testman()
        register_user(db, "tester", "pass2", "pass2")
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        drop_tables()
        self.assertEqual(users[1].username, "tester")

    def test_should_raise_exception_with_non_matching_passwords(self):
        with self.assertRaises(Exception):
            register_user(db, "testman", "password", "password1")
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        drop_tables()
        self.assertEqual(len(users), 0)

    def test_login_user_should_return_true_with_correct_credentials(self):
        register_testman()
        res = login_user(db, "testman", "password")
        self.assertEqual(res, True)

    def test_should_raise_exception_when_login_non_existing(self):
        with self.assertRaises(Exception):
            login_user(db, "testman", "password")

    def test_should_raise_exception_when_login_with_wrong_password(self):
        register_testman()
        with self.assertRaises(Exception):
            login_user(db, "testman", "password1")


