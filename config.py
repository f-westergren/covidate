from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config():
	SECRET_KEY = environ.get('SECRET_KEY') or 'you-will-never-guess'
	FLASK_APP = environ.get('FLASK_APP')
	FLASK_ENV = environ.get('FLASK_ENV')
		
	SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'postgres:///covid')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	