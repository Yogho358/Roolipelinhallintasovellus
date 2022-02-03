from app import app
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

uri = getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = uri

db = SQLAlchemy(app)

@app.route("/")
def index():
    db.session.execute("INSERT INTO test (txt) VALUES ('testi')");
    result = db.session.execute("SELECT * FROM test")
    res = result.fetchone()
    return render_template("index.html", res = res)