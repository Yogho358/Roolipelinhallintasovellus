
from flask import redirect, render_template, request, session
import src.users as users
from os import getenv, urandom



def configure_routes(app, db):

    app.secret_key = getenv("SECRET_KEY")

    @app.route("/")
    def index():
        
        if session and session["username"]:
            return render_template("frontpage.html")
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
               user = users.login_user(db, username, password)
               session["user_id"] = user.id
               session["username"] = user.username
               session["csrf"] = urandom(16).hex()
               return redirect("/")
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
            users.register_user(db, username, password1, password2)
            return redirect("/")

    @app.route("/logout")
    def logout():
        del session["user_id"]
        del session["username"]
        del session["csrf"]
        return redirect("/")

    @app.route("/characters")
    def characters():
        return render_template("characters.html")

    @app.route("/newcharacter", methods = ["GET", "POST"])
    def newcharacter():
        if request.method == "GET":
            return render_template("newcharacter.html")





