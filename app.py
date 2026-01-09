from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
import Database as db

app = Flask(__name__)
app.secret_key = "chave_secreta_para_sessions"



@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")


@app.route('/')
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))
    return render_template("index.html")


@app.route('/alimentos')
def alimentos():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))
    return render_template("alimentos.html")


@app.route('/alugar')
def alugar():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))
    return render_template("alugar.html")


@app.route('/contato')
def contato():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))
    return render_template("contato.html")


@app.route('/criarConta', methods=['GET'])
def criar_conta():
    return render_template("criarConta.html")


@app.route('/minhas')
def minhas():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))

    user_email = session.get("user_email")

    rented_game = db.get_rented_game(user_email)  

    return render_template("minhas.html", rented_game=rented_game)




@app.route('/api/criar_conta', methods=['POST'])
def api_criar_conta():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Preencha todos os campos."}), 400

    if db.read_user(email):
        return jsonify({"success": False, "message": "Email já cadastrado."}), 409

    db.insert_user(name, email, password)

    return jsonify({"success": True, "message": "Conta criada com sucesso!"})



@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Email e senha são obrigatórios."}), 400

    user = db.check_login(email, password)

    if user:
        session["logged_in"] = True
        session["user_email"] = user["email"]
        session["user_name"] = user["name"]

        return jsonify({
            "success": True,
            "message": f"Bem-vindo(a), {user['name']}!",
            "redirect": "/"
        })

    return jsonify({"success": False, "message": "Email ou senha incorretos."}), 401



@app.route('/logout')
def logout():
    if session.get("logged_in"):
        user_email = session.get("user_email")

        if user_email:
            db.clear_game_rented_by(user_email)

        session.clear()

    return redirect(url_for("login_page"))




@app.route('/reservar')
def reservar_jogo():
    if not session.get("logged_in"):
        return redirect(url_for("login_page"))

    game_id = request.args.get('game')

    if not game_id:
        return redirect(url_for('alugar'))

    game_map = {
        'arkhan': 'Arkham',
        'trivial': 'Trivial Pursuit',
        'madness': 'Madness',
        'ritual': 'Nosferatu',
        'mist-house': 'Eldritch',
        'whisper': 'Halloween',
        'underground': 'Dreadful Circus'
    }

    game_name = game_map.get(game_id)

    if not game_name:
        return redirect(url_for('alugar'))

    rented_by = db.check_game_rented(game_name)

    if rented_by:
        error_msg = f"O jogo '{game_name}' já foi alugado!"
        return redirect(url_for('alugar', error=error_msg))

    db.update_game_rented_by(game_name, session["user_email"])

    return redirect(url_for('minhas'))




@app.route('/api/get_rented_game', methods=['POST'])
def get_rented_game():
    data = request.get_json()
    email = data.get('email')
    game = db.get_rented_game(email)
    return jsonify({"game": game})




@app.route('/api/devolver_jogo', methods=['POST'])
def devolver_jogo():
    data = request.get_json()
    email = data.get('email')

    rented_game = db.get_rented_game(email)

    if not rented_game:
        return jsonify({"success": False, "message": "Nenhum jogo alugado."}), 400

    db.clear_game_rented_by_user(email, rented_game)

    return jsonify({"success": True, "message": f"Jogo '{rented_game}' devolvido com sucesso!"})




@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory("static", filename)




if __name__ == '__main__':
    db.add_rented_by_column()  
    db.init()
    db.initial_stock()
    app.run(debug=True)
