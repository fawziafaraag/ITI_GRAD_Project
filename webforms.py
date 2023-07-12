from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Regexp

# Create Register Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=5, message='Username must be at least 5 characters long'),
        ])
    email = StringField('Email Address', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long'),
        Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', message='Password must contain at least one letter and one number')
    ])
    cpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit_reg = SubmitField('Register')

   
    

# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=5, message='Username must be at least 5 characters long')
        ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
        ])
    submit_log = SubmitField("Log In")
