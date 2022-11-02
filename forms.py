from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import InputRequired, Optional, Length, EqualTo

class UserForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=64)])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), Length(min=8, max=64), EqualTo("password")])
    submit = SubmitField("Submit")