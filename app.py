from enum import auto
from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, login_required

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

from forms import RegistrationForm, LoginForm

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

@app.get('/login/')
def get_login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.post('/login/')
def post_login():
    # form = LoginForm()
    # if form.validate():
    #     # try to get the user associated with this email address
    #     user = User.query.filter_by(email=form.email.data).first()
    #     # if this user exists and the password matches
    #     if user is not None and user.verify_password(form.password.data):
    #         # log this user in through the login_manager
    #         login_user(user)
    #         # redirect the user to the page they wanted or the home page
    #         next = request.args.get('next')
    #         if next is None or not next.startswith('/'):
    #             next = url_for('index')
    #         return redirect(next)
    #     else: # if the user does not exist or the password is incorrect
    #         # flash an error message and redirect to login form
    #         flash('Invalid email address or password')
    #         return redirect(url_for('get_login'))
    # else: # if the form was invalid
    #     # flash error messages and redirect to get login form again
    #     for field, error in form.errors.items():
    #         flash(f"{field}: {error}")
    #     return redirect(url_for('get_login'))
    pass

@app.route('/')
@app.get('/register/')
def get_register():
    form = RegistrationForm()
    return render_template("register.html", form=form)


@app.post('/register/')
def post_register():
    form = RegistrationForm()
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
    return render_template('study.html')

@app.route('/quiz/')
def quiz():
    return render_template('quiz.html')

@app.route('/grades/')
def grades():
    return render_template('grades.html')

# @app.get('/logout/')
# @login_required
# def get_logout():
#     logout_user()
#     flash('You have been logged out')
#     return redirect(url_for('index'))