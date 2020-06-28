from flask import Blueprint, render_template
from flask import current_app as current_app
from flask_login import current_user

#Blueprint Configuration
index_bp = Blueprint(
	'index_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

@index_bp.route('/')
def index():
	""" Show index page with search form """

	return render_template("index.html", user=current_user)