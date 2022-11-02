from enum import auto
from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy

import os, sys
from requests import delete

from forms import UserForm

from sqlalchemy import null
script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(script_dir)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'aquickbrownfoxjumpedoverthelazydog'

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "library.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Users'
    email = db.Column(db.Unicode, primary_key=True)
    first_name = db.Column(db.Unicode, nullable=False)
    last_name = db.Column(db.Unicode, nullable=False)
    #password_hash = db.Column()

with app.app_context():
    db.create_all()

# we can remove this later down the line
@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/login/')
def login():
    return redirect(url_for('home'))

@app.get('/register/')
def get_register():
    form = UserForm()
    return render_template("register.html", form=form)

@app.post('/register/')
def post_register():
    form = UserForm()
    if form.validate() and not (User.query.filter_by(email=form.email.data.lower()).first()):
        # form data is valid. Add it to session and redirect
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data.lower()
        user = User(first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        # flash error messages for all validation problems
        if User.query.filter_by(email=form.email.data.lower()).first().email:
            flash(f"Email already in use")
        for field,error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))

@app.route('/study/')
def study():
    pass

@app.route('/quiz/')
def quiz():
    pass

@app.route('/grades/')
def grades():
    pass