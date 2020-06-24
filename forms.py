from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	email = StringField('Username', validators=[DataRequired(), Email(message='Enter a valid email')])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	confirm = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')
	
