from flask_wtf import FlaskForm
import artwork_dataloader
from wtforms.fields import StringField, SubmitField, EmailField, PasswordField, RadioField, BooleanField, SelectField, HiddenField
from wtforms.validators import ValidationError, InputRequired, Optional, Length, EqualTo, Regexp
from cropper import crop
import os
script_dir = os.path.dirname(__file__)
import string
import cropper


# random string generator
def gen_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))

import random
class qa(FlaskForm):
    pass
class RegistrationForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=8, max=64), EqualTo("password")])
    is_instructor = RadioField("I am a: ", choices=[(False,'Student'),(True,'Teacher')], validators=[InputRequired()])
    class_code = StringField("Class Code", validators=[Optional(), Regexp("^[a-zA-Z0-9_]*$", message="Class codes may only contain letters, numbers, and underscores")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log In")

class StudyForm(FlaskForm):
    archaic = BooleanField("Archaic")
    classical = BooleanField("Classical")
    hellenistic = BooleanField("Hellenistic")
    romanesque = BooleanField("Romansque")
    gothic = BooleanField("Gothic")
    renaissance = BooleanField("Renaissance")
    northern = BooleanField("Northern Renaissance")
    aristocratic = BooleanField("Aristocratic Baroque")
    dutch = BooleanField("Dutch Baroque")
    neoclassical = BooleanField("Neoclassical")
    romantic = BooleanField("Romantic")
    impressionism = BooleanField("Impressionism")
    post_impressionism = BooleanField("Post-impressionism")
    cubism = BooleanField("Cubism")
    post_modernism = BooleanField("Post-modernism")
    surrealism = BooleanField("Surrealism")
    abstract = BooleanField("Abstract")
    baroqueMusic = BooleanField("Baroque Music")
    classicalMusic = BooleanField("Classical Music")
    romanticMusic = BooleanField("Romantic Music")
    contemporaryMusic = BooleanField("Contemporary Music")
    submit = SubmitField("Submit")

class QuizSelectionForm(FlaskForm):
    archaic = BooleanField("Archaic")
    classical = BooleanField("Classical")
    hellenistic = BooleanField("Hellenistic")
    romanesque = BooleanField("Romansque")
    gothic = BooleanField("Gothic")
    renaissance = BooleanField("Renaissance")
    northern = BooleanField("Northern Renaissance")
    aristocratic = BooleanField("Aristocratic Baroque")
    dutch = BooleanField("Dutch Baroque")
    neoclassical = BooleanField("Neoclassical")
    romantic = BooleanField("Romantic")
    impressionism = BooleanField("Impressionism")
    post_impressionism = BooleanField("Post-impressionism")
    cubism = BooleanField("Cubism")
    post_modernism = BooleanField("Post-modernism")
    surrealism = BooleanField("Surrealism")
    abstract = BooleanField("Abstract")
    baroqueMusic = BooleanField("Baroque Music")
    classicalMusic = BooleanField("Classical Music")
    romanticMusic = BooleanField("Romantic Music")
    contemporaryMusic = BooleanField("Contemporary Music")
    submit = SubmitField("Submit")

class QuizForm(FlaskForm):
    q1 = RadioField(label = "s", choices = [])
    q2 = RadioField(label = "s", choices = [])
    q3 = RadioField(label = "s", choices = [])
    q4 = RadioField(label = "s", choices = [])
    q5 = RadioField(label = "s", choices = [])
    q6 = RadioField(label = "s", choices = [])
    q7 = RadioField(label = "s", choices = [])
    q8 = RadioField(label = "s", choices = [])
    q9 = RadioField(label = "s", choices = [])
    q10 = RadioField(label = "s", choices = [])
    answers = ""
    images = []
    submit = SubmitField(label = "Submit")
    def generateQuestions(self, pieces):
        self.images = []
        qtypes = ['What is the title of this art work?', 'What year was this art work made in?', 'Who made this art work?']
        titles = []
        artists = []
        years = []
        #get title, artist, and dates for all pieces in the selected range
        for piece in pieces:
            if piece['title'] not in titles:
                titles.append(piece['title'])
            if piece['artist'] not in artists:
                artists.append(piece['artist'])
            if piece['year'] not in years:
                years.append(piece['year'])
        
        art_dir = os.path.join(script_dir, "static\Artworks Database\Artpieces")
        for field, value in self._fields.items():
            #determine the type of question the user will be asked
            qtype = random.randint(0,2)

            #pick art work for client to identify

            piece = pieces[random.randint(0, len(pieces) - 1)] 
            filename = piece['title'] + ".jpg"
            piece_dir = os.path.join(art_dir, filename)
            self.images.append(cropper.crop(0.25, piece_dir))

            choices = []
            #add correct answer to choices
            answer = None
            if(qtype == 0):
                answer = piece['title']
            elif(qtype == 1):
                answer = random.randint(piece['year'][0], piece['year'][1])
            else:
                answer = piece['artist']
            choices.append(answer)
            
            #add 3 incorrect answers to choices
            if qtype == 0:
                random.shuffle(titles)
                i = 0
                while len(choices) < 4:
                    if titles[i] != piece['title']:
                        choices.append(titles[i])
                    i += 1
            elif qtype == 1:
                random.shuffle(years)
                i = 0
                while len(choices) < 4:
                    test = random.randint(years[i][0], years[i][1])
                    if test not in range(piece['year'][0], piece['year'][1] + 1):
                        choices.append(test)
                    i += 1
            else:
                random.shuffle(artists)
                i = 0
                while len(choices) < 4:
                    if artists[i] != piece['artist']:
                        choices.append(artists[i])
                    i += 1
            random.shuffle(choices)

            #add correct answer to form answers
            if answer == choices[0]:
                self.answers += "A"
            elif answer == choices[1]:
                self.answers += "B"
            elif answer == choices[2]:
                self.answers += "C"
            else:
                self.answers += "D"

            #assign each choise 'A' 'B' 'C' and 'D'
            for i in range(0, 4):
                choices[i] = (chr(i + 65), choices[i])

            if isinstance(value, RadioField):
                value.label = qtypes[qtype]
                value.choices = choices
    
