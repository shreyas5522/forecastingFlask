from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=4, max=20)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Sign Up')
