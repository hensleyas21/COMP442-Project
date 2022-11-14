import os
import json
from datetime import datetime
from marshmallow import Schema, fields, validate, post_load

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

# get the full path to the directory containing this file
script_dir = os.path.abspath(os.path.dirname(__file__))
jsonfile = os.path.join(script_dir, 'pieces.json')
with open(jsonfile, 'rt', encoding='utf-8') as fin:
    jsondata = json.load(fin)

# convert this data using Schemas
pieces = []
for piece_id, piece_data in jsondata.items():
    piece = piece_data
    pieces.append(piece)
