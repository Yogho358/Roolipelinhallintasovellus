
from os import getenv


from flask_sqlalchemy import SQLAlchemy

def get_db(app):
    uri = getenv("DATABASE_URL")

    if not uri:
        uri = "postgresql+psycopg2://"

    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = uri

    return SQLAlchemy(app)
