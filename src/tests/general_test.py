
import unittest
import character_repository
import games
import weapons
from flask import Flask
from db import get_db
from users import register_user, login_user, get_user



app = Flask(__name__)
db = get_db(app)

def register_testman():
    register_user(db, "testman", "password", "password")

def register_3_users():
    register_testman()
    register_user(db, "testman2", "password", "password")
    register_user(db, "testman3", "password", "password")

def create_3_games():
    games.create_game(db, "testgame", 1)
    games.create_game(db, "testgame2", 1)
    games.create_game(db, "testgame3", 2)

def add_3_users_to_games():
    games.add_player_to_game(db, 2, 1)
    games.add_player_to_game(db, 3, 1)
    games.add_player_to_game(db, 1, 2)

def create_character():
    character_repository.create_character(db, 1, "test")

def create_weapons():
    weapons.create_weapon(db, 'nyrkki', 1, 2, 30, 30, 'small', 'Käsi puristettuna palloon')
    weapons.create_weapon(db, "pitkämiekka", 2, 6, 50, 50, "big", "miekka,joka on pitkä")
    weapons.create_weapon(db, 'perhosmiekat', 2, 6, 50, 50, 'big', 'yksi per käsi')
    

def create_three_games_and_add_characters():
    character_repository.create_character(db, 1, "test")
    character_repository.create_character(db, 2, "test2")
    character_repository.create_character(db, 3, "test3")
    character_repository.add_character_to_game(db,1,2)
    character_repository.add_character_to_game(db,2,2)
    character_repository.add_character_to_game(db,3,3)

def drop_tables():
    db.session.execute("DROP TABLE IF EXISTS playersingames;")
    db.session.execute("DROP TABLE IF EXISTS weaponsingames;")
    db.session.execute("DROP TABLE IF EXISTS test;")
    db.session.execute("DROP TABLE IF EXISTS users;")
    
    db.session.execute("DROP TABLE IF EXISTS characters;")
    db.session.execute("DROP TABLE IF EXISTS games;")
    db.session.execute("DROP TABLE IF EXISTS weapons;")
    
    

class TestStuff(unittest.TestCase):
    
    

    def setUp(self): 
        
        drop_tables()
        db.session.execute("CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);")
        db.session.execute("CREATE TABLE games (id SERIAL PRIMARY KEY, name TEXT NOT NULL, game_master_id INTEGER);")
        db.session.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL);")
        
        db.session.execute("CREATE TABLE playersingames (user_id INTEGER REFERENCES users, game_id INTEGER REFERENCES games);")
        db.session.execute("CREATE TABLE weapons (id SERIAL PRIMARY KEY, name TEXT NOT NULL, min_damage INTEGER, max_damage INTEGER, attack_modifier INTEGER, defence_modifier INTEGER, size TEXT, description TEXT);")
        db.session.execute("CREATE TABLE weaponsingames (weapon_id INTEGER REFERENCES weapons, game_id INTEGER REFERENCES games);")
        db.session.execute("CREATE TABLE characters (id SERIAL PRIMARY KEY, user_id INTEGER, name TEXT NOT NULL, current_hp INTEGER, max_hp INTEGER, attack_skill INTEGER, defence_skill INTEGER, game_id INTEGER REFERENCES games, weapon_id INTEGER REFERENCES weapons);")
        create_weapons()

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

    def test_get_user_should_return_user_by_id_from_db(self):
        register_testman()
        user = get_user(db, 1)
        self.assertEqual(user.username, "testman")

    def test_get_players_for_game_should_return_list_of_all_players_in_a_game_by_game_id(self):
        register_3_users()
        create_3_games()
        db.session.execute("INSERT INTO playersingames (user_id, game_id) VALUES (2,1);")
        db.session.execute("INSERT INTO playersingames (user_id, game_id) VALUES (3,1);")
        db.session.execute("INSERT INTO playersingames (user_id, game_id) VALUES (1,2);")
        players_in_game_1 = games.get_players_for_game(db, 1)
        self.assertEqual(len(players_in_game_1), 2)
        players_in_game_2 = games.get_players_for_game(db, 2)
        self.assertEqual(len(players_in_game_2), 1)

    def test_add_players_to_game_should_save_info_to_playersingames(self):
        register_3_users()
        create_3_games()
        add_3_users_to_games()
        players_in_game_1 = games.get_players_for_game(db, 1)
        self.assertEqual(len(players_in_game_1), 2)
        players_in_game_2 = games.get_players_for_game(db, 2)
        self.assertEqual(len(players_in_game_2), 1)

    def test_should_not_be_able_to_add_player_to_game_more_than_once(self):
        register_3_users()
        create_3_games()
        add_3_users_to_games()
        with self.assertRaises(Exception):
            games.add_player_to_game(db, 2, 1)
        players_in_game_1 = games.get_players_for_game(db, 1)
        self.assertEqual(len(players_in_game_1), 2)

    def test_remove_player_from_game_should_remove_user_from_playersingames(self):
        register_3_users()
        create_3_games()
        add_3_users_to_games()
        games.remove_player_from_game(db, 2, 1)
        players_in_game_1 = games.get_players_for_game(db, 1)
        self.assertEqual(len(players_in_game_1), 1)

    def test_change_character_health_with_decrease(self):
        create_character()
        character_repository.change_character_health(db,1,5,20,20,False)
        character = character_repository.get_character(db,1)
        self.assertEqual(character.current_hp, 15)

    def test_change_character_health_with_increase(self):
        create_character()
        character_repository.change_character_health(db,1,5,20,20,False)
        character_repository.change_character_health(db,1,2,15,20,True)
        character = character_repository.get_character(db,1)
        self.assertEqual(character.current_hp, 17)

    def test_change_health_should_not_increase_over_max(self):
        create_character()
        character_repository.change_character_health(db,1,5,20,20,False)
        character_repository.change_character_health(db,1,200,15,20,True)
        character = character_repository.get_character(db,1)
        self.assertEqual(character.current_hp, 20)
    
    def test_can_create_weapon(self):
        weapons.create_weapon(db, "longsword",1,5,50,50,"big", "a long sword")
        result = db.session.execute("SELECT * FROM weapons;")
        res = result.fetchall()
        self.assertEqual(res[3].name, "longsword")

    def test_get_available_weapons_for_games_should_return_all_weapons_with_empty_input(self):
        res = games.get_weapons_available_for_game(db, 1)
        self.assertEqual(len(res), 3)

    def test_should_be_able_to_add_weapons_to_games(self):
        create_3_games()
        
        games.add_weapon_to_game(db,1,1)
        result = db.session.execute("SELECT * FROM weaponsingames;")
        self.assertEqual(len(result.fetchall()), 1)

    def test_should_be_able_to_get_weapons_in_game(self):
        create_3_games()
        
        games.add_weapon_to_game(db, 1, 1)
        games.add_weapon_to_game(db,2,1)
        res = games.get_weapons_in_game(db,1)
        self.assertEqual(len(res), 2)

    def test_should_be_able_to_remove_weapon_from_game(self):
        create_3_games()
        
        games.add_weapon_to_game(db, 1, 1)
        games.add_weapon_to_game(db,2,1)
        games.remove_weapon_from_game(db,1,1)
        res = games.get_weapons_in_game(db,1)
        self.assertEqual(len(res), 1)

    def test_should_be_able_to_add_character_to_game(self):
        register_testman()
        create_character()
        create_3_games()
        character_repository.add_character_to_game(db, 1, 2)
        res = db.session.execute("SELECT * FROM characters WHERE game_id = 2")
        self.assertEqual(len(res.fetchall()), 1)

    def test_should_get_all_characters_in_game_by_id(self):
        register_3_users()
        create_3_games()
        create_three_games_and_add_characters()
        res = games.get_all_characters_in_game(db, 2)
        self.assertEqual(len(res), 2)

    def test_should_be_able_to_remove_character_from_game_by_character_id(self):
        register_3_users()
        create_3_games()
        create_three_games_and_add_characters()
        character_repository.remove_character_from_game(db, 2)
        res = games.get_all_characters_in_game(db, 2)
        self.assertEqual(len(res), 1)

    def test_should_be_able_to_remove_all_characters_of_a_user_from_a_game(self):
        register_3_users()
        create_3_games()
        create_three_games_and_add_characters()
        character_repository.create_character(db, 1, "test4")
        character_repository.add_character_to_game(db, 4, 2)
        games.remove_all_characters_from_game(db, 1, 2)
        res = games.get_all_characters_in_game(db, 2)
        self.assertEqual(len(res), 1)

    def test_create_character_should_add_nyrkki_as_weapon(self):
        register_testman()
        character_repository.create_character(db, 1, "test")
        character = character_repository.get_character(db, 1)
        weapon = weapons.get_weapon(db, character.weapon_id)
        self.assertEqual(weapon.name, "nyrkki")

    def test_find_default_weapon_should_find_nyrkki(self):
        weapon_id = weapons.get_default_weapon_id(db)
        self.assertEqual(weapon_id, 1)

    def test_set_weapon_should_set_weapon(self):
        create_character()
        character_repository.set_weapon(db, 1, 2)
        character = character_repository.get_character(db, 1)
        weapon = weapons.get_weapon(db, character.weapon_id)
        self.assertEqual(weapon.name, "pitkämiekka")