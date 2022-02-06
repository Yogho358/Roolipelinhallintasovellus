DROP TABLE IF EXISTS test;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS characters;

DROP TABLE IF EXISTS games;

DROP TABLE IF EXISTS playersingames;

CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);

CREATE TABLE games (id SERIAL PRIMARY KEY, name TEXT, game_master_id INTEGER);

CREATE TABLE characters (id SERIAL PRIMARY KEY, user_id INTEGER, name TEXT, current_hp INTEGER, max_hp INTEGER);

CREATE TABLE playersingames (user_id INTEGER, game_id INTEGER);

INSERT INTO characters (user_id, name, current_hp, max_hp) VALUES (1, 'testihahmo1', 20, 20);
INSERT INTO characters (user_id, name, current_hp, max_hp) VALUES (1, 'testihahmo2', 20, 20);
INSERT INTO characters (user_id, name, current_hp, max_hp) VALUES (2, 'testihahmo3', 20, 20);
INSERT INTO games (name, game_master_id) VALUES ('testipeli1', 1);
INSERT INTO games (name, game_master_id) VALUES ('testipeli2', 1);
