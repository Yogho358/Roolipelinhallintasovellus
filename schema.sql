DROP TABLE IF EXISTS test;

DROP TABLE IF EXISTS users;

CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);

CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);