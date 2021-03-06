from flask_login import UserMixin, LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask.json import JSONEncoder
from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()

login = LoginManager()
login.login_view = 'auth_bp.login'
login.login_message_category = "danger"

class User(UserMixin, db.Model):
	""" Users """

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String, nullable=False, unique=True)
	email = db.Column(db.String, nullable=False)
	password = db.Column(db.Text, nullable=False)

	searches = db.relationship('Search', backref="user")

	def __repr__(self):
		return f'<User id={self.id} name={self.username} email={self.email}>'
	
	@classmethod
	def signup(cls, username, email, password):
		"""Register user with hashed password and return user"""
	
		hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

		user = User(
			username=username,
			email=email,
			password=hashed_pwd,
		)
		
		db.session.add(user)
		return user

	@classmethod
	def authenticate(cls, username, password):
		"""Validate that user exists & password is correct.

		Return user if valid, else return false.
		"""
		u = User.query.filter_by(username=username).first()

		if u and bcrypt.check_password_hash(u.password, password):
			#return user instance
			return u
		else:
			return False
			
class Search(db.Model):
	""" Searches """

	__tablename__ = 'searches'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	location = db.Column(db.String, nullable=False)
	date = db.Column(db.String, nullable=False)
	dates = db.Column(db.Text, nullable=False)
	cases = db.Column(db.Text, nullable=False)
	change_cases = db.Column(db.Text, nullable=False)
	deaths = db.Column(db.Text, nullable=False)
	change_deaths = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False)
	description = db.Column(db.Text)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

	def __repr__(self):
		return f'<Search id={self.id} location={self.location} date={self.date} user_id={self.user_id}>'

	@classmethod
	def create(cls, searchObj):
		""" Create a new search instance """

		search = Search(
			location=searchObj['location'],
			date=searchObj['date'],
			dates=searchObj['dates'],
			deaths=searchObj['deaths'],
			change_deaths=searchObj['change_deaths'],
			cases=searchObj['cases'],
			change_cases=searchObj['change_cases'],
			created_at=datetime.now(),
			description=searchObj['description']
		)

		return search	

	def serialize(self):
		return {
			'location': self.location,
			'date': self.date,
			'dates': self.dates,
			'deaths': self.deaths,
			'change_deaths': self.change_deaths,
			'cases': self.cases,
			'change_cases': self.change_cases,
			'created_at': self.created_at.strftime('%m/%d/%Y'),
			'id': self.id
		}

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
		
