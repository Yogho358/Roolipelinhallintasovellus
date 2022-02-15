
from flask import redirect, render_template, request, session, abort
import src.users as users
import src.character_repository as character_repository
import src.games as game_repository
from os import getenv, urandom



def configure_routes(app, db):

    app.secret_key = getenv("SECRET_KEY")

    def check_user():
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
        
        mastered_games = game_repository.get_mastered_games(db, session["user_id"])
        all_games = game_repository.get_all_games(db)
        
        return render_template("frontpage.html", mastered_games = mastered_games, all_games = all_games)
        
        
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
            try:
                username = request.form["username"]
                password1 = request.form["password1"]
                password2 = request.form["password2"]
                users.register_user(db, username, password1, password2)
                return redirect("/")
            except Exception as e:
                print(e)
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

    @app.route("/character/<int:character_id>", methods = ["GET", "POST"])
    def show_character(character_id):
        if not check_user():
            return redirect("/login")
        character = character_repository.get_character(db, character_id)
        if character.user_id != session["user_id"]:
            return redirect("/")
        if request.method == "GET":
            return render_template("character.html", character = character)

        if request.method == "POST":
            check_csrf()
            if request.form["modify_health"] == "increase":
                healing = True
            else:
                healing = False
        
            amount = int(request.form["health_value"])
            character_repository.change_character_health(db, character.id, amount, character.current_hp, character.max_hp, healing)

            return redirect(f"/character/{character.id}")

    @app.route("/newgame", methods = ["POST"])
    def new_game():
        if not check_user():
            return redirect("/login")
        check_csrf()
        name = request.form["new_game_name"]
        game_repository.create_game(db, name, session["user_id"])
        return redirect("/")

    @app.route("/gameinfo/<int:game_id>", methods = ["GET", "POST"])
    def game_info(game_id):
        if not check_user():
            return redirect("/login")
        
        if request.method == "GET":
            game = game_repository.get_game(db, game_id)
            game_master = users.get_user(db, game.game_master_id)
            players = game_repository.get_players_for_game(db, game_id)
            in_game = game_repository.check_if_in_game(db, session["user_id"], game_id)
            return render_template("game_info.html", game = game, game_master = game_master, players = players, in_game = in_game)
        
        if request.method == "POST":
            check_csrf()
            try:
                game_repository.add_player_to_game(db, session["user_id"], game_id)
                return redirect(f"/gameinfo/{game_id}")
            except Exception as e:
                print(e)
                return redirect("/")

    @app.route("/managegame/<int:game_id>")
    def manage_game(game_id):
        if not check_user():
            return redirect("/login")
        
        game = game_repository.get_game(db, game_id)
        if game.game_master_id != session["user_id"]:
            return redirect("/")

        players = game_repository.get_players_for_game(db,game_id)

        return render_template("manage_game.html", game = game, players = players)

    @app.route("/leavegame/<int:game_id>", methods = ["POST"])
    def leave_game(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        game_repository.remove_player_from_game(db, session["user_id"], game_id)
        return redirect(f"/gameinfo/{game_id}")

    
