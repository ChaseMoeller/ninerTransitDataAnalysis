import scripts.users
import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import session

app = Flask(__name__)
#create session secret key
app.secret_key = "not secret"
@app.route('/')
@app.route('/home')
def home():
    if not session.get('LoggedIn'):
        return render_template("home.html", loggedIn = False)
    else:
        return render_template("home.html", loggedIn = True, name = session['Name'])

@app.route('/about')
def about():
    if not session.get('LoggedIn'):
        return render_template("about.html", loggedIn = False)
    else:
        return render_template("about.html", loggedIn = True, name = session['Name'])

@app.route('/login', methods=['GET'])
def login():
    if not session.get('LoggedIn'):
        return render_template("login.html", loggedIn = False)
    else:
        return render_template("login.html", loggedIn = True, name = session['Name'])

@app.route('/login', methods=['POST'])
def authorize():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    if scripts.users.validate_user(first_name, last_name):
        session['Name'] = str(first_name + " " + last_name)
        session['LoggedIn'] = True
        flash("Login Successful") #make sure to retrieve flash message when visualize page is setup the css code for a successful flash message is under class name .flash-success
        return render_template("login.html", loggedIn = True, name = session['Name'])
    else:
        flash("Invalid credentials, try again")
        return render_template("login.html", loggedIn = False)

@app.route('/signup', methods=['GET'])
def serve_signup():
    if not session.get('LoggedIn'):
        return render_template("signup.html", loggedIn = False)
    else:
        return render_template("signup.html", loggedIn = True, name = session['Name'])

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    scripts.users.add_user(first_name, last_name)
    session['Name'] = str(first_name + " " + last_name)
    session['LoggedIn'] = True
    flash("Sign up successful and logged in!") #make sure to retrieve flash message when visualize page is setup the css code for a successful flash message is under class name .flash-success
    return render_template("login.html", loggedIn = True, name = session['Name'])

@app.route('/logout')
def logout():
    session.pop('LoggedIn', None)
    return redirect('/home')

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)
#new stuff