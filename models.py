from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	""" Users """

	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(30), nullable=False)
	location = db.Column(db.String)
	password = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		return f'<User id={self.id} name={self.name}>'
	
class Search(db.Model):
	""" Searches """

	__tablename__ = 'searches'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	location = db.Column(db.String, nullable=False)
	search_date = db.Column(db.DateTime, nullable=False)
	created_at = db.Column(db.DateTime, nullable=False)
	description = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

	def __repr__(self):
		return f'<Search id={self.id} location={self.location} search_date={self.search_date} user_id={self.user_id}>'

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)