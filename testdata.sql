DROP TABLE IF EXISTS test;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS characters;

CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);

CREATE TABLE characters (id SERIAL PRIMARY KEY, user_id INTEGER, name TEXT);

INSERT INTO characters (user_id, name) VALUES (1, "testihahmo1")
INSERT INTO characters (user_id, name) VALUES (1, "testihahmo2")
INSERT INTO characters (user_id, name) VALUES (2, "testihahmo3")