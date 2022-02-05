from flask import Flask
from src.routes import configure_routes
from src.db import get_db

# def main():

#     app = Flask(__name__)
#     db = get_db(app)

#     configure_routes(app, db)

# if __name__ == "__main__":
#     main()

app = Flask(__name__)
db = get_db(app)

configure_routes(app, db)

