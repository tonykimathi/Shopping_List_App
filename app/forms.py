from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm = PasswordField('Confirm Password')
    remember = BooleanField('Remember me')


class Shoppinglist_nameForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=5)])


class ShoppingitemForm(FlaskForm):
    """For used to create a shopping list item"""
    name = StringField('Name', validators=[InputRequired(), Length(min=5)])
    quantity = StringField('quantity', validators=[InputRequired()])





