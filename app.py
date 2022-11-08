from enum import auto
from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user

import os, sys
from requests import delete

import os
from password_hashing import UpdatedHasher
# find your pepper file
scriptdir = os.path.dirname(__file__)
pepfile = os.path.join(scriptdir, "pepper.bin")
# read your pepper key from the file
with open(pepfile, 'rb') as fin:
    pepper_key = fin.read()
# create a new UpdatedHasher with pepper key
pwd_hasher = UpdatedHasher(pepper_key)

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
    password_hash = db.Column(db.LargeBinary, nullable=False)
    is_instructor = db.Column(db.Boolean, nullable=False)
    class_code = db.Column(db.Unicode, nullable=True)

    # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")
    @password.setter
    def password(self, pwd):
        self.password_hash = pwd_hasher.hash(pwd)

    # add a verify_password convenience method
    def verify_password(self, pwd):
        return pwd_hasher.check(pwd, self.password_hash)


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
    if (form.validate() 
        and not (User.query.filter_by(email=form.email.data.lower()).first())
        and not (form.is_instructor.data == 'True' and not form.class_code.data)
        and not (form.is_instructor.data == 'True' and User.query.filter_by(class_code=form.class_code.data.lower()).first())
        and not (form.is_instructor.data == 'False' and form.class_code.data and not User.query.filter_by(class_code=form.class_code.data.lower()).first())):
        # form data is valid. Add it to session and redirect
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        is_instructor = False
        if (form.is_instructor.data == 'True'):
            is_instructor = True
        class_code = form.class_code.data.lower()
        user = User(first_name=first_name, last_name=last_name, email=email, password=password, is_instructor=is_instructor, class_code=class_code)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        # flash error messages for all validation problems
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already in use")
        elif form.is_instructor.data == 'True' and not form.class_code.data:
            flash("Class code needed to create an instructor account")
        elif form.is_instructor.data == 'True' and User.query.filter_by(class_code=form.class_code.data.lower()).first():
            flash("Class code already taken, please use a different code")
        elif form.is_instructor.data == 'False' and form.class_code.data and not User.query.filter_by(class_code=form.class_code.data.lower()).first():
            flash("Invalid class code, please try a different code")
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