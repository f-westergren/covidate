from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	email = StringField('Username', validators=[DataRequired(), Email(message='Enter a valid email')])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	remember_me = BooleanField('Remember Me')
	


	# confirm = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])