import os

from flask import Flask, render_template
from flask_login import current_user

from models import connect_db, login
from config import Config

# Import blueprints
from auth.auth import auth_bp
from search.search import search_bp
from user.user import user_bp

app = Flask(__name__)
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(search_bp)
app.register_blueprint(user_bp)

connect_db(app)
login.init_app(app)

@app.route('/')
def index():
	""" Show index page with search form """

	return render_template("index.html", user=current_user, color="#FFF199")

@app.route('/about')
def about():
	""" Show about page """
	return render_template("about.html", color="#E4FDE1")