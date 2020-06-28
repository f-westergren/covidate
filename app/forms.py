from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	remember_me = BooleanField('Remember Me')
	
class SearchForm(FlaskForm):
	location = StringField('Location', validators=[DataRequired()])
	date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(message='Please enter a valid date, (MM-DD-YY).')])
	description = StringField('Description')

class SignupForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	confirm = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
	email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email')])