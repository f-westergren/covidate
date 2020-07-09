import os

class Config():
	DEBUG = False
	TESTING = True

	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql:///covid'
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'youwillneverknow'