
from flask import redirect, render_template, request, session, abort
import src.users as users
import src.character_repository as character_repository
import src.games as game_repository
import src.weapons as weapon_repository
from os import getenv, urandom



def configure_routes(app, db):

    app.secret_key = getenv("SECRET_KEY")

    def check_user():
        return session and session["username"]
            
    def check_csrf():
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    def check_game_master(game_id):
        game = game_repository.get_game(db, game_id)
        if game.game_master_id != session["user_id"]:
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
            characters_to_add = character_repository.get_users_characters(db, session["user_id"])
            characters_in_game = game_repository.get_all_characters_in_game(db, game_id)

            return render_template("game_info.html", game = game, game_master = game_master, players = players, in_game = in_game, characters_to_add = characters_to_add, characters_in_game = characters_in_game)
        
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
            abort(403)
        players = game_repository.get_players_for_game(db,game_id)
        weapons = game_repository.get_weapons_in_game(db, game_id)
        available_weapons = game_repository.get_weapons_available_for_game(db, game_id)
        sizes = [(0,"pieni"),(1,"iso")]

        return render_template("manage_game.html", game = game, players = players, weapons = weapons, available_weapons = available_weapons, sizes = sizes)

    @app.route("/addweapontogame/<int:game_id>", methods = ["POST"])
    def add_weapon_to_game(game_id):
       check_csrf()
       check_game_master(game_id)
       game_repository.add_weapon_to_game(db,request.form["weapons"], game_id)
       return redirect(f"/managegame/{game_id}")

    @app.route("/addcharactertogame/<int:game_id>", methods = ["POST"])
    def add_character_to_game(game_id):
        check_csrf()
        character_repository.add_character_to_game(db, request.form["characters_to_add"], game_id)
        return redirect(f"/gameinfo/{game_id}")


    @app.route("/removeweaponfromgame/<int:game_id>", methods =["POST"])
    def remove_weapon_from_game(game_id):
        check_csrf()
        check_game_master(game_id)
        weapon_id = request.form["weapon_id"]
        game_repository.remove_weapon_from_game(db, weapon_id, game_id)
        return redirect(f"/managegame/{game_id}")

    @app.route("/leavegame/<int:game_id>", methods = ["POST"])
    def leave_game(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        game_repository.remove_player_from_game(db, session["user_id"], game_id)
        game_repository.remove_all_characters_from_game(db, session["user_id"], game_id)
        return redirect(f"/gameinfo/{game_id}")

    @app.route("/removecharacterfromgame/<int:game_id>", methods = ["POST"])
    def remove_character_from_game(game_id):
        check_csrf()
        character_id = request.form["character_id"]
        character_repository.remove_character_from_game(db, character_id)
        return redirect(f"/gameinfo/{game_id}")

    @app.route("/createweapon/<int:game_id>", methods = ["POST"])
    def create_weapon(game_id):
        check_csrf()
        name = request.form["weapon_name"]
        min_damage = request.form["min_damage"]
        max_damage = request.form["max_damage"]
        attack_modifier = request.form["attack_modifier"]
        defence_modifier = request.form["defence_modifier"]
        size = request.form["size"]      
        if size == "0":
            size = "small"
        if size == "1":
            size = "big"
        desciption = request.form["description"]
        weapon_repository.create_weapon(db, name, min_damage, max_damage, attack_modifier, defence_modifier, size, desciption)
        return redirect(f"/managegame/{game_id}")
    
