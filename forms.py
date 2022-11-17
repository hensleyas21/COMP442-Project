from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, EmailField, PasswordField, RadioField, BooleanField
from wtforms.validators import InputRequired, Optional, Length, EqualTo, Regexp

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

