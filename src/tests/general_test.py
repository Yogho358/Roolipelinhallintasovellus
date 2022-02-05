
import unittest
import characters
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
    db.session.execute("DROP TABLE IF EXISTS characters;")

class TestStuff(unittest.TestCase):
    
    

    def setUp(self): 
        
        drop_tables()
        db.session.execute("CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);")
        db.session.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);")
        db.session.execute("CREATE TABLE characters (id SERIAL PRIMARY KEY,user_id INTEGER, name TEXT);")

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

    def test_login_user_should_return_usr_object_with_correct_credentials(self):
        register_testman()
        res = login_user(db, "testman", "password")
        drop_tables()
        self.assertEqual(res.id, 1)

    def test_should_raise_exception_when_login_non_existing(self):
        with self.assertRaises(Exception):
            login_user(db, "testman", "password")

    def test_should_raise_exception_when_login_with_wrong_password(self):
        register_testman()
        with self.assertRaises(Exception):
            login_user(db, "testman", "password1")
        drop_tables()

    def test_create_character_should_save_character_to_db(self):
        register_testman()
        characters.create_character(db, 1, "test")
        result = db.session.execute("SELECT * FROM characters;")
        chars = result.fetchall()
        drop_tables()
        self.assertEqual(len(chars), 1)

    def test_get_users_characters_should_return_list_of_all_characters_of_a_user(self):
        characters.create_character(db, 1, "test")
        characters.create_character(db, 1, "test")
        characters.create_character(db, 2, "test")
        res = characters.get_users_characters(db, 1)
        drop_tables()
        self.assertEqual(len(res), 2)
