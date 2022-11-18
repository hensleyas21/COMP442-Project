import os
import json
from datetime import datetime
from marshmallow import Schema, fields, validate, post_load
from flask import Flask
from sqlalchemy import null
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'aquickbrownfoxjumpedoverthelazydog'

scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "art.sqlite3")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# create simple objects for art pieces
class Painting:
    def __init__(self, year, artist, title):
        self.title = title
        self.artist = artist
        self.year = year

class Music:
    def __init__(self, year, composer, title):
        self.year = year
        self.composer = composer
        self.title = title

class PiecePainting(db.Model):
    __tablename__ = 'paintings'
    #title = db.Column(db.Unicode, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.Unicode, nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)

class PieceMusic(db.Model):
    __tablename__ = 'music'
    title = db.Column(db.Unicode, primary_key=True)
    composer = db.Column(db.Unicode, nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)

# get the full path to the directory containing this file
script_dir = os.path.abspath(os.path.dirname(__file__))
jsonfile = os.path.join(script_dir, 'static/Artworks Database/pieces.json')
with open(jsonfile, 'rt', encoding='utf-8') as fin:
    jsondata = json.load(fin)


# filter pieces based on form input
def filter(filters):
    pieces = []
    for piece_id, piece_data in jsondata.items():
        for filter in filters:
            if piece_data.get('subtype') == filter:
                piece = piece_data
                pieces.append(piece)
    return pieces
