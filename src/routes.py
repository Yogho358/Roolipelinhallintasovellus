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
    result = db.session.execute("SELECT txt FROM test")
    messages = result.fetchall()
    return render_template("index.html", count=len(messages), messages=messages)