import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG_TB_INTERCEPT_REDIRECTS = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'postgresql:///covid-event-search'
	TEMPLATES_AUTO_RELOAD = True
	