from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    game_state = db.Column(db.Text, nullable=True)

@app.route('/')
def home():
    return redirect(url_for('game'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Elimina el ID del usuario de la sesión
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('game'))
        return 'Login failed. Check your credentials.'

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, game_state=None)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return 'Username already exists.'

    return render_template('register.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    if user is None:
        flash('Usuario no encontrado. Por favor, vuelva a iniciar sesión.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        game_state = request.form.get('game_state')
        # Verifica que game_state no esté vacío antes de guardarlo
        if game_state:
            try:
                json.loads(game_state)  # Verifica que sea JSON válido
                user.game_state = game_state
            except json.JSONDecodeError:
                flash('Error al guardar el estado del juego. Formato JSON inválido.', 'error')
        else:
            flash('Estado del juego vacío. No se guardó nada.', 'warning')
        db.session.commit()

    # Recuperar el estado del juego o establecer un estado inicial
    if user.game_state:
        try:
            game_state = json.loads(user.game_state)
        except json.JSONDecodeError:
            flash('Error al cargar el estado del juego. Formato JSON inválido.', 'error')
            game_state = {
                "selected": [],
                "values": [5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000],
                "revealed": []
            }
    else:
        game_state = {
            "selected": [],
            "values": [5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000],
            "revealed": []
        }

    # Asegurar que game_state es un diccionario para evitar errores
    if not isinstance(game_state, dict):
        game_state = {
            "selected": [],
            "values": [5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000, 2000000, 5000000],
            "revealed": []
        }

    # Para depuración, imprime game_state
    print(f"game_state: {game_state}")

    return render_template('game.html', values=game_state['values'], game_state=json.dumps(game_state), revealed=game_state['revealed'])

if __name__ == '__main__':
    app.run(debug=True)
