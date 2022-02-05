
from flask import redirect, render_template, request, session
from os import getenv
from src.users import register_user, login_user


def configure_routes(app, db):

    app.secret_key = getenv("SECRET_KEY")

    @app.route("/")
    def index():
        
        
        if session:
            return render_template("frontpage.html", session = session)
        else:
            return redirect("/login")
        
    @app.route("/login", methods = ["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template("login.html")

        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            try:
                login_user(db, username, password)
                session["username"] = username
            except Exception as e:
                print(e)

            
        
            return redirect("/")

    @app.route("/register", methods = ["GET", "POST"])
    def register():
        if request.method == "GET":
            return render_template("register.html")

        if request.method == "POST":
            username = request.form["username"]
            password1 = request.form["password1"]
            password2 = request.form["password2"]
            register_user(db, username, password1, password2)
            return redirect("/")

    @app.route("/logout")
    def logout():
        del session["username"]
        return redirect("/")




