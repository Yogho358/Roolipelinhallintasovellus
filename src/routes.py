
#from tkinter import E
from flask import redirect, render_template, request, session, abort
import src.npc_repository as npc_repository
import src.users as users
import src.character_repository as character_repository
import src.games as game_repository
import src.weapons as weapon_repository
from os import getenv, urandom
from src.error import Error



def configure_routes(app, db):

    app.secret_key = getenv("SECRET_KEY")

    err = Error()

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

        error = err.error
        err.error = None
        
        mastered_games = game_repository.get_mastered_games(db, session["user_id"])
        all_games = game_repository.get_all_games(db)
        
        return render_template("frontpage.html", mastered_games = mastered_games, all_games = all_games, error = error)
        
        
    @app.route("/login", methods = ["GET", "POST"])
    def login():
        if request.method == "GET":
            error = err.error
            err.error = None
            return render_template("login.html", error = error)

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
                err.error = e
                return redirect("/")
            
        
            

    @app.route("/register", methods = ["GET", "POST"])
    def register():
        
        if request.method == "GET":
            error = err.error
            err.error = None
            return render_template("register.html", error = error)

        if request.method == "POST":
            try:
                username = request.form["username"]
                password1 = request.form["password1"]
                password2 = request.form["password2"]
                users.register_user(db, username, password1, password2)
                return redirect("/")
            except Exception as e:
                err.error = e
                return redirect("/register")

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
            error = err.error
            err.error = None
            return render_template("newcharacter.html", error = error)

        if request.method == "POST":
            check_csrf()
            name = request.form["character_name"]
            default_weapon_id = weapon_repository.get_default_weapon_id(db)
            try:
                character_repository.create_character(db, session["user_id"], name, 20, default_weapon_id)
                return redirect("/characters")
            except Exception as e:
                err.error = e
                return redirect("/newcharacter")

    @app.route("/character/<int:character_id>", methods = ["GET", "POST"])
    def show_character(character_id):
        if not check_user():
            return redirect("/login")
        character = character_repository.get_character(db, character_id)
        if character.user_id != session["user_id"]:
            return redirect("/")


        if request.method == "GET":
            game = game_repository.get_game(db, character.game_id)
            weapon = weapon_repository.get_weapon(db, character.weapon_id)
            available_weapons = None
            if game:
                available_weapons = game_repository.get_weapons_in_game(db, game.id)
            return render_template("character.html", character = character, game = game, weapon = weapon, available_weapons = available_weapons)

        if request.method == "POST":
            check_csrf()
            if request.form["modify_health"] == "increase":
                healing = True
            else:
                healing = False

            amount = request.form["health_value"]
            if len(amount) == 0:
                amount = 0
            amount = int(amount)
            character_repository.change_character_health(db, character.id, amount, character.current_hp, character.max_hp, healing)

            return redirect(f"/character/{character.id}")

    @app.route("/npc/<int:npc_id>", methods = ["GET", "POST"])
    def show_npc(npc_id):
        if not check_user():
            return redirect("/login")
        character = npc_repository.get_npc(db, npc_id)

        if request.method == "GET":
            weapon = weapon_repository.get_weapon(db, character.weapon_id)
            weapons = weapon_repository.get_all_weapons(db)
            return render_template("/npc.html", character = character, weapon = weapon, weapons = weapons)

        if request.method == "POST":
            check_csrf()
            if request.form["modify_health"] == "increase":
                healing = True
            else:
                healing = False

            amount = request.form["health_value"]
            if len(amount) == 0:
                amount = 0
            amount = int(amount)
            npc_repository.change_npc_health(db, npc_id, amount, character.current_hp, character.max_hp, healing)
            return redirect(f"/npc/{character.id}")

    @app.route("/changecharacterweapon/<int:character_id>", methods =["POST"])
    def change_character_weapon(character_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        character_repository.set_weapon(db,character_id, request.form["weapons"])
        return redirect(f"/character/{character_id}")

    @app.route("/changenpcweapon/<int:npc_id>", methods =["POST"])
    def change_npc_weapon(npc_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        npc_repository.set_weapon(db, npc_id, request.form["weapons"])
        return redirect(f"/npc/{npc_id}")

    @app.route("/newgame", methods = ["POST"])
    def new_game():
        if not check_user():
            return redirect("/login")
        check_csrf()
        name = request.form["new_game_name"]
        try:
            game_id = game_repository.create_game(db, name, session["user_id"])
            weapon_id = weapon_repository.get_default_weapon_id(db)
            game_repository.add_weapon_to_game(db, weapon_id, game_id)
            return redirect("/")
        except Exception as e:
            err.error = e
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
            player_count = game_repository.get_number_of_players_in_game(db, game_id)

            return render_template("game_info.html", game = game, game_master = game_master, players = players, in_game = in_game, characters_to_add = characters_to_add, characters_in_game = characters_in_game, player_count = player_count)
        
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
        error = err.error
        err.error = None
        game = game_repository.get_game(db, game_id)
        if game.game_master_id != session["user_id"]:
            abort(403)
        players = game_repository.get_players_for_game(db,game_id)
        weapons = game_repository.get_weapons_in_game(db, game_id)
        available_weapons = game_repository.get_weapons_available_for_game(db, game_id)
        sizes = [(0,"pieni"),(1,"iso")]
        npc_templates = npc_repository.get_npc_templates(db)
        npcs = game_repository.get_npcs_in_game(db, game_id)
        all_weapons = weapon_repository.get_all_weapons(db)
        characters_in_game = game_repository.get_all_characters_in_game(db, game_id)
        return render_template("manage_game.html", game = game, players = players, weapons = weapons, available_weapons = available_weapons, sizes = sizes, error = error, npc_templates = npc_templates, all_weapons = all_weapons, npcs = npcs, characters_in_game = characters_in_game)

    @app.route("/addweapontogame/<int:game_id>", methods = ["POST"])
    def add_weapon_to_game(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        check_game_master(game_id)
        try:
            game_repository.add_weapon_to_game(db,request.form["weapons"], game_id)
            return redirect(f"/managegame/{game_id}")
        except Exception as e:
            err.error = e
            return redirect(f"/managegame/{game_id}")

    @app.route("/addnpctogame/<int:game_id>", methods = ["POST"])
    def add_npc_to_game(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        check_game_master(game_id)
        try:
            npc = npc_repository.get_npc(db, request.form["npcs"])
            print(npc)
            name = request.form["npc_name"]
            npc_repository.add_npc_to_game(db, game_id, npc.template_name, name, npc.max_hp, npc.attack_skill, npc.defence_skill, npc.weapon_id, npc.description)
            return redirect(f"/managegame/{game_id}")
        except Exception as e:
            err.error = e
            return redirect(f"/managegame/{game_id}")

    @app.route("/addcharactertogame/<int:game_id>", methods = ["POST"])
    def add_character_to_game(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        character_repository.add_character_to_game(db, request.form["characters_to_add"], game_id)
        return redirect(f"/gameinfo/{game_id}")


    @app.route("/removeweaponfromgame/<int:game_id>", methods =["POST"])
    def remove_weapon_from_game(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        check_game_master(game_id)
        weapon_id = request.form["weapon_id"]
        game_repository.remove_weapon_from_game(db, weapon_id, game_id)
        return redirect(f"/managegame/{game_id}")

    @app.route("/removenpcfromgame/<int:game_id>", methods = ["POST"])
    def remove_npc_from_game(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        check_game_master(game_id)
        npc_id = request.form["npc_id"]
        npc_repository.delete_npc(db, npc_id)
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
        if not check_user():
            return redirect("/login")
        check_csrf()
        character_id = request.form["character_id"]
        character_repository.remove_character_from_game(db, character_id)
        return redirect(f"/gameinfo/{game_id}")

    @app.route("/createweapon/<int:game_id>", methods = ["POST"])
    def create_weapon(game_id):
        if not check_user():
            return redirect("/login")
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
        try:
            weapon_repository.create_weapon(db, name, min_damage, max_damage, attack_modifier, defence_modifier, size, desciption)
            return redirect(f"/managegame/{game_id}")
        except Exception as e:
            err.error = e
            return redirect(f"/managegame/{game_id}")

    @app.route("/createnpc/<int:game_id>", methods = ["POST"])
    def create_npc(game_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        template_name = request.form["npc_name"]
        name = f"{template_name}_template"
        hp = request.form["hp"]
        attack_skill = request.form["attack_skill"]
        defence_skill = request.form["defence_skill"]
        weapon_id = request.form["npc_weapon"]
        description = request.form["description"]
        try:
            npc_repository.create_npc(db,template_name, name, hp, attack_skill, defence_skill, weapon_id, description)
            return redirect(f"/managegame/{game_id}")
        except Exception as e:
            err.error = e
            return redirect(f"/managegame/{game_id}")


    @app.route("/setmaxdamageweapon/<int:game_id>/<int:character_id>", methods = ["POST"])
    def set_maximum_damage_weapon(game_id, character_id):
        if not check_user():
            return redirect("/login")
        check_csrf()
        weapon_id = game_repository.get_highest_maximum_damage_weapon_id_in_game(db, game_id)
        character_repository.set_weapon(db, character_id, weapon_id)
        return redirect(f"/character/{character_id}")

    @app.route("/modifycharacter/<int:character_id>", methods = ["GET", "POST"])
    def modify_character(character_id):
        return modify_character_npc(character_id, False, request.method)
        
    @app.route("/modifynpc/<int:npc_id>", methods = ["GET", "POST"])
    def modify_npc(npc_id):
        return modify_character_npc(npc_id, True, request.method)

    def modify_character_npc(id, npc, method):
        if not check_user():
            return redirect("/login")
        if not npc:
            character = character_repository.get_character(db, id)
            url = "character"
            repository = character_repository
        else:
            character = npc_repository.get_npc(db, id)
            url = "npc"
            repository = npc_repository
        if method == "GET":
            return render_template(f"modify_{url}.html", character = character)
        if method == "POST":
            check_csrf()
            hp = request.form["hp"]
            if not hp:
                hp = character.max_hp
            attack_skill = request.form["attack_skill"]
            if not attack_skill:
                attack_skill = character.attack_skill
            defence_skill = request.form["defence_skill"]
            if not defence_skill:
                defence_skill = character.defence_skill
            description = request.form["description"]
            if not description:
                description = character.description
            name = request.form["name"]
            if not name:
                name = character.name
            try:
                repository.modify_character(db, character.id, name, hp, attack_skill, defence_skill)
                return redirect(f"/{url}/{character.id}")
            except Exception as e:
                err.error = e
                return redirect(f"/{url}/{character.id}")

    @app.route("/createbattle/<int:game_id>")
    def create_battle(game_id):
        if not check_user():
            return redirect("/login")
        check_game_master(game_id)  
        pcs = game_repository.get_all_characters_in_game(db, game_id)
        npcs = game_repository.get_npcs_in_game(db, game_id)
        return render_template("create_battle.html", pcs = pcs, npcs = npcs)

        

    @app.route("/createbattle", methods = ["POST"])
    def battle():
        check_csrf()
        pc_ids = request.form.getlist("pc")
        if pc_ids:
            pcs = character_repository.get_characters_based_on_ids(db, pc_ids)
            pc_weapons = weapon_repository.get_pc_weapons_in_battle(db, pc_ids)
            easiest_pc_targets = character_repository.get_easiest_target_pc(db, pc_ids)
        else:
            pcs = None
            pc_weapons = None
            easiest_pc_targets = None
        npc_ids = request.form.getlist("npc")
        if npc_ids:
           npcs = npc_repository.get_npcs_based_on_ids(db, npc_ids)
           npc_weapons = weapon_repository.get_npc_weapons_in_battle(db, npc_ids)
           easiest_npc_targets = npc_repository.get_easiest_target_npc(db, npc_ids)
        else:
            npcs = None
            npc_weapons = None
            easiest_npc_targets = None
        
        return render_template("battle.html", pcs = pcs, npcs = npcs, pc_weapons = pc_weapons, npc_weapons = npc_weapons, easiest_pc_targets = easiest_pc_targets, easiest_npc_targets = easiest_npc_targets)