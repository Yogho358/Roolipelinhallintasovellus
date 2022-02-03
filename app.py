from flask import Flask
from src.routes import configure_routes
from src.db import get_db



app = Flask(__name__)
db = get_db(app)

configure_routes(app, db)

