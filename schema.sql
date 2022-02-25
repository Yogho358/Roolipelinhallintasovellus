DROP TABLE IF EXISTS playersingames;

DROP TABLE IF EXISTS weaponsingames;

DROP TABLE IF EXISTS test;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS characters;

DROP TABLE IF EXISTS games;

DROP TABLE IF EXISTS weapons;



CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL CHECK (username != ''), password TEXT NOT NULL CHECK (password != ''));

CREATE TABLE games (id SERIAL PRIMARY KEY, name TEXT NOT NULL, game_master_id INTEGER);

CREATE TABLE playersingames (user_id INTEGER REFERENCES users, game_id INTEGER REFERENCES games);

CREATE TABLE weapons (id SERIAL PRIMARY KEY, name TEXT NOT NULL, min_damage INTEGER, max_damage INTEGER, attack_modifier INTEGER, defence_modifier INTEGER, size TEXT, description TEXT);

CREATE TABLE weaponsingames (weapon_id INTEGER REFERENCES weapons, game_id INTEGER REFERENCES games);

CREATE TABLE characters (id SERIAL PRIMARY KEY, user_id INTEGER, name TEXT NOT NULL CHECK (name != ''), current_hp INTEGER, max_hp INTEGER, attack_skill INTEGER, defence_skill INTEGER, game_id INTEGER REFERENCES games, weapon_id INTEGER REFERENCES weapons);

INSERT INTO weapons (name, min_damage, max_damage, attack_modifier, defence_modifier, size, description) VALUES ('Pitkämiekka', 2, 6, 50, 50, 'big', 'miekka, joka on pitkä');

INSERT INTO weapons (name, min_damage, max_damage, attack_modifier, defence_modifier, size, description) VALUES ('Perhosmiekat', 2, 6, 50, 50, 'small', 'yksi per käsi');

INSERT INTO weapons (name, min_damage, max_damage, attack_modifier, defence_modifier, size, description) VALUES ('Nyrkki', 1, 2, 30, 30, 'small', 'Käsi puristettuna palloon');
