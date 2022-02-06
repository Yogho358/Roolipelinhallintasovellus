
import unittest
import character_repository
import games
from flask import Flask
from db import get_db
from users import register_user, login_user, get_user



app = Flask(__name__)
db = get_db(app)

def register_testman():
        register_user(db, "testman", "password", "password")

def create_3_games():
    games.create_game(db, "testgame", 1)
    games.create_game(db, "testgame2", 1)
    games.create_game(db, "testgame3", 2)

def drop_tables():
    db.session.execute("DROP TABLE IF EXISTS test;")
    db.session.execute("DROP TABLE IF EXISTS users;")
    db.session.execute("DROP TABLE IF EXISTS characters;")
    db.session.execute("DROP TABLE IF EXISTS games;")
    db.session.execute("DROP TABLE IF EXISTS playersingames;")

class TestStuff(unittest.TestCase):
    
    

    def setUp(self): 
        
        drop_tables()
        db.session.execute("CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);")
        db.session.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);")
        db.session.execute("CREATE TABLE characters (id SERIAL PRIMARY KEY, user_id INTEGER, name TEXT, current_hp INTEGER, max_hp INTEGER);")
        db.session.execute("CREATE TABLE games (id SERIAL PRIMARY KEY, name TEXT, game_master_id INTEGER);")
        db.session.execute("CREATE TABLE playersingames (user_id INTEGER, game_id INTEGER);")

    def tearDown(self):
        drop_tables()
        

    def test_db_testing(self):
        db.session.execute("INSERT INTO test (txt) VALUES ('testi');")
        result = db.session.execute("SELECT * FROM test;")
        res = result.fetchall()
        self.assertEqual(res[0].txt, "testi")

    def test_should_save_user_to_db_on_registration(self):  
        register_testman()
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        self.assertEqual(len(users), 1)

    def test_should_save_users_with_right_name_on_registration(self):
        register_testman()
        register_user(db, "tester", "pass2", "pass2")
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        self.assertEqual(users[1].username, "tester")

    def test_should_raise_exception_with_non_matching_passwords(self):
        with self.assertRaises(Exception):
            register_user(db, "testman", "password", "password1")
        result = db.session.execute("SELECT * FROM users;")
        users = result.fetchall()
        self.assertEqual(len(users), 0)

    def test_login_user_should_return_usr_object_with_correct_credentials(self):
        register_testman()
        res = login_user(db, "testman", "password")
        self.assertEqual(res.id, 1)

    def test_should_raise_exception_when_login_non_existing(self):
        with self.assertRaises(Exception):
            login_user(db, "testman", "password")

    def test_should_raise_exception_when_login_with_wrong_password(self):
        register_testman()
        with self.assertRaises(Exception):
            login_user(db, "testman", "password1")

    def test_create_character_should_save_character_to_db(self):
        register_testman()
        character_repository.create_character(db, 1, "test")
        result = db.session.execute("SELECT * FROM characters;")
        chars = result.fetchall()
        self.assertEqual(len(chars), 1)

    def test_get_users_characters_should_return_list_of_all_characters_of_a_user(self):
        character_repository.create_character(db, 1, "test")
        character_repository.create_character(db, 1, "test")
        character_repository.create_character(db, 2, "test")
        res = character_repository.get_users_characters(db, 1)
        self.assertEqual(len(res), 2)

    def test_get_character_should_return_character_based_on_id(self):
        character_repository.create_character(db, 1, "test")
        character_repository.create_character(db, 1, "test2")
        res = character_repository.get_character(db, 2)
        self.assertEqual(res.name, "test2")

    def test_create_game_should_save_game_to_db(self):
        games.create_game(db, "testgame", 1)
        games.create_game(db, "testgame2", 1)
        result = db.session.execute("SELECT * FROM games;")
        all_games = result.fetchall()
        self.assertEqual(len(all_games), 2)

    def test_get_master_games_should_return_list_of_games_mastered_by_user_id(self):
        create_3_games()
        mastered_games = games.get_mastered_games(db, 1)
        self.assertEqual(len(mastered_games), 2)

    def test_get_all_games_should_return_all_games_from_db(self):
        create_3_games()
        all_games = games.get_all_games(db)
        self.assertEqual(len(all_games), 3)

    def test_get_game_should_return_game_by_id_from_db(self):
        create_3_games()
        game = games.get_game(db, 2)
        self.assertEqual(game.name, "testgame2")

    def test_get_user_should_return_user_by_idfrom_db(self):
        register_testman()
        user = get_user(db, 1)
        self.assertEqual(user.username, "testman")

    def test_get_players_for_game_should_return_list_of_all_players_in_a_game_by_game_id(self):
        register_testman()
        register_user(db, "testman2", "password", "password")
        register_user(db, "testman3", "password", "password")
        create_3_games()
        db.session.execute("INSERT INTO playersingames (user_id, game_id) VALUES (2,1);")
        db.session.execute("INSERT INTO playersingames (user_id, game_id) VALUES (3,1);")
        db.session.execute("INSERT INTO playersingames (user_id, game_id) VALUES (1,2);")
        players_in_game_1 = games.get_players_for_game(db, 1)
        self.assertEqual(len(players_in_game_1), 2)
        players_in_game_2 = games.get_players_for_game(db, 2)
        self.assertEqual(len(players_in_game_2), 1)
