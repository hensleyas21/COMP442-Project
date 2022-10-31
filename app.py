from enum import auto
from flask import Flask, request, render_template, redirect, url_for, abort
from flask import flash
from flask_sqlalchemy import SQLAlchemy

import os, sys

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

@app.route('/')
@app.get('/login/')
def login():
    pass

@app.get('/register/')
def get_register():
    pass

@app.post('/register/')
def post_register():
    pass

@app.get('/study/')
def study():
    pass

@app.get('/quiz/')
def quiz():
    pass

@app.get('/grades/')
def grades():
    pass