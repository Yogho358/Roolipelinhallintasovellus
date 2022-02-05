
from flask import redirect, render_template, request, session, abort
import src.users as users
import src.characters as character_repository
from os import getenv, urandom



def configure_routes(app, db):

    app.secret_key = getenv("SECRET_KEY")

    def check_user():
        print(session)
        if session and session["username"]:
            return True
        else:
            return False

    def check_csrf():
        print(request.form["csrf_token"])
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    @app.route("/")
    def index():
        if not check_user():
            return redirect("/login")
        
        return render_template("frontpage.html")
        
        
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
               session["csrf_token"] = urandom(16).hex()
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
        del session["csrf_token"]
        return redirect("/")

    @app.route("/characters")
    def characters():
        if not check_user():
            return redirect("/login")

        my_characters = character_repository.get_users_characters(db, session["user_id"])
        return render_template("characters.html", characters = my_characters)

    @app.route("/newcharacter", methods = ["GET", "POST"])
    def newcharacter():
        if not check_user():
            return redirect("/login")

        if request.method == "GET":
            return render_template("newcharacter.html")

        if request.method == "POST":
            check_csrf()
            name = request.form["character_name"]
            character_repository.create_character(db, session["user_id"], name)
            return redirect("/characters")




