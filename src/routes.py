
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from src.db import get_db
from os import getenv


def configure_routes(app):

    db = get_db(app)

    @app.route("/")
    def index():
        db.session.execute("INSERT INTO test (txt) VALUES ('testi')");
        result = db.session.execute("SELECT * FROM test")
        res = result.fetchall()
        return render_template("index.html", res = res)