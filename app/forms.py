from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
	email = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
	remember_me = BooleanField('Remember Me')
	
class SearchForm(FlaskForm):
	location = StringField('Location', validators=[DataRequired()])
	date = DateField('Date', validators=[DataRequired()])
	description = StringField('Description')

	# confirm = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])

	# Email(message='Enter a valid email')]