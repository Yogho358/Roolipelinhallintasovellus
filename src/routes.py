
from flask import redirect, render_template, request, session
from os import getenv


def configure_routes(app, db):

    app.secret_key = getenv("SECRET_KEY")

    @app.route("/")
    def index():
        print(session)
        
        if session:
            return render_template("frontpage.html", session = session)
        else:
            return redirect("/login")
        
    @app.route("/login", methods = ["GET"])
    def login():
        return render_template("login.html")

    @app.route("/register")
    def register():
        return render_template("register.html")

    @app.route("/login", methods = ["POST"])
    def handle_login():
        username = request.form["username"]
        password = request.form["password"]

        session["username"] = username
        
        return redirect("/")

    @app.route("/logout")
    def logout():
        del session["username"]
        return redirect("/")
