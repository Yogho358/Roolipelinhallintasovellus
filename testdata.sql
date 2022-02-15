DROP TABLE IF EXISTS playersingames;

DROP TABLE IF EXISTS weaponsingames;

DROP TABLE IF EXISTS test;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS characters;

DROP TABLE IF EXISTS games;

DROP TABLE IF EXISTS weapons;

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);

CREATE TABLE games (id SERIAL PRIMARY KEY, name TEXT NOT NULL, game_master_id INTEGER);

CREATE TABLE characters (id SERIAL PRIMARY KEY, user_id INTEGER, name TEXT NOT NULL, current_hp INTEGER, max_hp INTEGER, attack_skill INTEGER, defence_skill INTEGER);

CREATE TABLE playersingames (user_id INTEGER REFERENCES users, game_id INTEGER REFERENCES games);

CREATE TABLE weapons (id SERIAL PRIMARY KEY, name TEXT NOT NULL, min_damage INTEGER, max_damage INTEGER, attack_modifier INTEGER, defence_modifier INTEGER, size TEXT, description TEXT);

CREATE TABLE weaponsingames (weapon_id INTEGER REFERENCES weapons, game_id INTEGER REFERENCES games);

INSERT INTO characters (user_id, name, current_hp, max_hp) VALUES (1, 'testihahmo1', 20, 20);
INSERT INTO characters (user_id, name, current_hp, max_hp) VALUES (1, 'testihahmo2', 20, 20);
INSERT INTO characters (user_id, name, current_hp, max_hp) VALUES (2, 'testihahmo3', 20, 20);
INSERT INTO games (name, game_master_id) VALUES ('testipeli1', 1);
INSERT INTO games (name, game_master_id) VALUES ('testipeli2', 1);
