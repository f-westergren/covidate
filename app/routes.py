from flask import redirect, render_template, url_for, request, flash, session, jsonify
from flask_cors import cross_origin, CORS
from werkzeug.urls import url_parse
from sqlalchemy.exc import IntegrityError
import requests
import wtforms_json

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from app.forms import LoginForm, SearchForm, SignupForm
from app.models import User, Search
from app.helper import get_state_and_county, get_covid_data

from app import app, db

cors = CORS(app, resources={r'/search': {"origins": "*"}})
wtforms_json.init()

@app.route('/')
def index():
	""" Show index page with search form """

	return render_template("index.html", user=current_user)

##############################################################################
# Login, logout and register routes

@app.route('/login', methods=['GET', 'POST'])
def login():
	""" Show login page with login form """

	if current_user.is_authenticated:
		return redirect(url_for('/'))
	
	form = LoginForm()

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.authenticate(username, password)

		if not user:
			flash("Invalid credentials.", 'danger')
			return redirect(url_for('login'))	

		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)

	return render_template('/user/login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	"""Handle user signup.

  Create new user and add to DB. Redirect to home page.

  If form not valid, present form.

  If the there already is a user with that username: flash message
  and re-present form.
  """

	if current_user.is_authenticated:
		return redirect(url_for('index'))

	form = SignupForm()

	if form.validate_on_submit():
		try:
			user = User.signup(
				username=form.username.data,
				password=form.password.data,
				email=form.email.data,
			)
			db.session.commit()

		except IntegrityError:
			flash('Username already taken', 'danger')
			return render_template('/user/signup.html', form=form)
		
		login_user(user)
		return redirect(url_for('index'))
	
	return render_template('user/signup.html', form=form)

##############################################################################
# User routes

# @app.route('/user/<username>')
# @login_required
# def user(username):
# 	""" Show user dashboard with three searches thumbnails """

# 	if username != current_user.username:
# 		return redirect('/')
	
# 	return render_template('user.html', user=user)

# @app.route('/user/<username>/profile', methods=['GET', 'POST'])
# @login_required
# def user_profile(username):
# 	""" Show user profile page with edit form """

@app.route('/user/<username>/searches')
@login_required
def searches(username):
	""" Show user's searches thumbnails """
	

	return render_template('/user/searches.html')

# @app.route('/user/<username>/delete', methods=['POST'])
# @login_required
# def delete_user(username)
# 	""" Delete user """

	# Password required for this

##############################################################################
# Search

@app.route('/search', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def search():
	print(session.get('date'))
	
	form = SearchForm.from_json(request.get_json(), csrf_enabled=False)

	# TODO: Make sure date is not before today's date.

	if form.validate():
		location = get_state_and_county(form.location.data)
		date = str(form.date.data)
		
		county = location['county'].lower()
		state = location['state'].lower()

		covid_data = get_covid_data(date, state, county)

		return jsonify(covid_data)
		


	return 'Nope!'

	""" Show search or search result """

	# Option to create account and save search?
	# If logged in, option to save search

# @app.route('/searches/<int:search_id>', methods=['GET', 'POST'])
# @login_required
# def search(search_id):
# 	""" Show and edit search """																

# @app.route('searches/<int:search_id>/delete')
# @login_required
# 	def delete_search(search_id):
# 		"""Delete saved search"""





