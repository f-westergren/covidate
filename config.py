import os
from secrets import SECRET

class Config():
	DEBUG = False
	TESTING = True

	SECRET_KEY = SECRET
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql:///covid'
