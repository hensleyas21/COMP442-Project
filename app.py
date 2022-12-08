from enum import auto
from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash, session
from flask_sqlalchemy import SQLAlchemy
import jinja2
from jinja2.ext import Extension
from forms import *
import artwork_dataloader as dataloader
import os, sys
from password_hashing import UpdatedHasher
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from PIL import Image
import random
import string
import cropper
import json

# random string generator
def gen_string():
    letters = string.ascii_lowercase
    file_name = ''.join(random.choice(letters) for i in range(10))
    file_name = file_name + '.jpg'
    return 

def save(dic):
    file = open('hash.json', 'a')
    stuff =json.dumps(dic)
    file.write(stuff)
    file.close()

def stringify(word):
    return str(word)

def jsonif(dic):
    return json.dump(dic)

# method that I call inside jinja to do the cropping
def cropper_weighted_random(percent, path):
    image = Image.open(path) 
    splitted = path.split('.')
    extension = '.' + splitted[len(splitted)-1]
    width = percent*image.size[0]
    x = random.randrange(image.size[0])
    length = percent*image.size[1]
    y = random.randrange(image.size[1])
    image_cropped = image.crop((x,y,x + width, y + length))
    #path = '/static/CroppedImages/_cropped/'
    name = gen_string() + extension
    filename = './static/Artworks Database/Artpieces/' + name
    image_cropped.save(filename)
    return name

# To shuffle elements of a list in jinja
def filter_shuffle(seq):
    try:
        result = list(seq)
        random.shuffle(result)
        return result
    except:
        return seq

def length(arr):
    return len(arr)

# find your pepper file
scriptdir = os.path.dirname(__file__)
pepfile = os.path.join(scriptdir, "pepper.bin")
# read your pepper key from the file
with open(pepfile, 'rb') as fin:
    pepper_key = fin.read()
# create a new UpdatedHasher with pepper key
pwd_hasher = UpdatedHasher(pepper_key)

script_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append

app = Flask(__name__)

#making the crop method a global one so that the jinja template can access it
app.jinja_env.globals.update(
    cropper_weighted_random=cropper_weighted_random, len=length, str=stringify, dump=jsonif, save=save)
    
app.jinja_env.add_extension('jinja2.ext.do')
app.jinja_env.filters['shuffle'] = filter_shuffle

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'aquickbrownfoxjumpedoverthelazydog'

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "library.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Prepare and connect the LoginManager to this app
app.login_manager = LoginManager()
app.login_manager.login_view = 'get_login'
@app.login_manager.user_loader
def load_user(email):
    return User.query.get(email)

class User(db.Model):
    __tablename__ = 'Users'
    email = db.Column(db.Unicode, primary_key=True)
    first_name = db.Column(db.Unicode, nullable=False)
    last_name = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)
    is_instructor = db.Column(db.Boolean, nullable=False)
    class_code = db.Column(db.Unicode, nullable=True)
    scores = db.relationship('Score', backref='user')

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
    
    def is_active(self):
        return current_user.email == self.email
    
    def get_id(self):
        return self.email

class Score(db.Model):
    __tablename__ = 'Scores'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.Unicode, db.ForeignKey('Users.email'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    num_correct = db.Column(db.Integer, nullable=False)
    num_total = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()



@app.route('/')
def home_redirect():
    return redirect(url_for('home'))

@app.route('/home/')
# @login_required
def home():
    return render_template('home.html', user=current_user)

@app.get('/login/')
def get_login():
    form = LoginForm()
    return render_template("login.html", form=form)

@app.post('/login/')
def post_login():
    form = LoginForm()
    if form.validate():
        # try to get the user associated with this email address
        user = User.query.filter_by(email=form.email.data).first()
        # if this user exists and the password matches
        if user is not None and user.verify_password(form.password.data):
            # log this user in through the login_manager
            login_user(user)
            # redirect the user to the page they wanted or the home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('home')
            return redirect(next)
        else: # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash('Invalid email address or password')
            return redirect(url_for('get_login'))
    else: # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))


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
            flash(f"{field}:{error}")
        return redirect(url_for('get_register'))

@app.get('/study/')
def get_study():
    form = StudyForm()
    return render_template('study.html', form=form, method='GET') 

@app.post('/study/')
def post_study():
    form = StudyForm()
    filters = []
    labels = {"archaic": "Archaic", "classical": "Classical", "hellenistic": "Hellenistic",
        "romanesque": "Romanesque", "gothic": "Gothic", "renaissance": "Renaissance",
        "northern": "Northern Renaissance", "aristocratic": "Aristocratic Baroque",
        "dutch": "Dutch Baroque", "neoclassical": "Neoclassical", "romantic": "Romantic",
        "impressionism": "Impressionism", "post_impressionism": "Post-impressionism",
        "cubism": "Cubism", "post_modernism": "Post-modernism", "surrealism": "Surrealism",
        "abstract": "Abstract", "baroqueMusic": "Baroque Music", "classicalMusic": "Classical Music",
        "romanticMusic": "Romantic Music", "contemporaryMusic": "Contemporary Music"
    }
    if form.validate():
        for key, value in form.data.items():
            if value and key!= 'submit':
                if key!='csrf_token':
                    filters.append(labels[key])
    pieces = dataloader.filter(filters)
    return render_template('study.html', method='POST', pieces = pieces)

@app.get('/quiz/')
def get_quiz():
    form = QuizSelectionForm()
    return render_template('quiz.html', form=form, method='GET')

@app.post('/quiz/')
def post_quiz():
    form = QuizSelectionForm()
    filters = []
    labels = {"archaic": "Archaic", "classical": "Classical", "hellenistic": "Hellenistic",
        "romanesque": "Romanesque", "gothic": "Gothic", "renaissance": "Renaissance",
        "northern": "Northern Renaissance", "aristocratic": "Aristocratic Baroque",
        "dutch": "Dutch Baroque", "neoclassical": "Neoclassical", "romantic": "Romantic",
        "impressionism": "Impressionism", "post_impressionism": "Post-impressionism",
        "cubism": "Cubism", "post_modernism": "Post-modernism", "surrealism": "Surrealism",
        "abstract": "Abstract", "baroqueMusic": "Baroque Music", "classicalMusic": "Classical Music",
        "romanticMusic": "Romantic Music", "contemporaryMusic": "Contemporary Music"
    }
    if form.validate():
        for key, value in form.data.items():
            if value and key!= 'submit':
                if key!='csrf_token':
                    filters.append(labels[key])
        pieces = dataloader.filter(filters)
        session['pieces'] = pieces
        return redirect('../test/')
    else:
        redirect(url_for('get_quiz'))

@app.get('/test/')
def get_test():
    try:
        qform = QuizForm()
        qform.generateQuestions(session['pieces'])        
    except:
        return redirect(url_for('get_quiz'))
    session.pop('pieces', None)
    session['answers']= qform.answers
    qfields = [value for field, value in qform._fields.items() if field[0] == 'q']
    print(qfields)
    questions = dict([(qform.images[i], qfields[i]) for i in range(0, len(qfields))])
    return render_template('test.html', form=qform, questions = questions)

@app.post('/test/')
def post_test():
    form = QuizForm(request.form)
    answers = ""
    score = 0
    for field, value in form.data.items():
        if(field[0] == 'q'):
            if value == None:
                answers += 'E'
            else:
                answers += value
    for i in range(0, len(answers)):
        if answers[i] == session['answers'][i]:    
            score = score + 1
    session.pop('answers', None)
    return str(score) + "/" + str(len(answers))

@app.route('/quizMode/<string:artworks>')
def get_quizMode(artworks):
    quizform = QuizForm()
    return render_template('quizMode.html', quizform=quizform, artworks=artworks)

@app.route('/grades/')
def grades():
    return render_template('grades.html')

@app.get('/logout/')
def get_logout():
    logout_user()
    return redirect(url_for('home'))

@app.get("/scores/")
def get_scores():
    if (current_user == None):
        redirect(url_for('get_login'))
    return render_template("scores.html", user=current_user)
    