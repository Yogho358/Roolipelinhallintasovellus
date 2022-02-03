import unittest
from flask import Flask
from db import get_db

def set_db():
    app = Flask(__name__)
    return get_db(app)

class TestDBTesting(unittest.TestCase):
    

    def setUp(self):

        self.db = set_db()
        
        self.db.session.execute("DROP TABLE IF EXISTS test;")
        self.db.session.execute("DROP TABLE IF EXISTS users;")
        self.db.session.execute("CREATE TABLE test (id SERIAL PRIMARY KEY, txt TEXT);")
        self.db.session.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);")

    def test_db_testing(self):

        self.db.session.execute("INSERT INTO test (txt) VALUES ('testi')")
        result = self.db.session.execute("SELECT * FROM test")
        res = result.fetchall()
        self.assertEqual(res[0].txt, "testi")

