import scripts.users
import os
import bcrypt

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session
from database import db_init, db
from models import User as User
from forms import RegisterForm
from forms import LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "not secret"

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    if session.get('user'):
        return render_template("home.html", user=session['user'])
    return render_template("home.html")

@app.route('/about')
def about():
    if not session.get('LoggedIn'):
        return render_template("about.html", loggedIn = False)
    else:
        return render_template("about.html", loggedIn = True, name = session['Name'])

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id
            return redirect(url_for('home'))
        login_form.password.errors = ["Incorrect username or password."]
        return render_template("login.html", form=login_form)
    else:
        return render_template("login.html", form=login_form)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        new_user = User(first_name, last_name, request.form['email'], h_password)
        db.session.add(new_user)
        db.session.commit()
        session['user'] = first_name
        session['user_id'] = new_user.id

        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('home'))

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
#new stuff