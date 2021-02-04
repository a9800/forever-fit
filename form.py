from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField

class RegisterForm(FlaskForm):
    username = StringField('username')
    first_name = StringField('fname')
    last_name = StringField('lname')
    fitness_goals = StringField('goals')
    dob = StringField('birthday')
    password = StringField('psw')

class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('psw')
    submit = SubmitField('Submit')