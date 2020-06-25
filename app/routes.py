from flask import redirect, render_template, url_for, request, flash, session
from werkzeug.urls import url_parse
import requests
from datetime import date

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from app.forms import LoginForm, SearchForm
from app.models import User, Search

from app import app, db

@app.route('/', methods=['GET', 'POST'])
def index():
	""" Show index page with search form """

	form = SearchForm()

	if form.validate_on_submit():
		location = form.location.data
		date = form.date.data
		description = form.description.data or None
		# Set user_id if user is logged in.
		user_id = current_user.id if current_user.is_authenticated else None
		
		search = Search(
			location=location, 
			date=date,
			description=description,  
			created_at=date.today(), 
			user_id=user_id
		)

		print('search', search)
		
		db.session.add(search)
		db.session.commit()

		session['search'] = search.id

		return redirect(url_for('searches'))

	return render_template("index.html", user=current_user, form=form)

##############################################################################
# Login, logout and register routes

@app.route('/login', methods=['GET', 'POST'])
def login():
	""" Show login page with login form """

	if current_user.is_authenticated:
		return redirect(url_for('/'))
	
	form = LoginForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data
		user = User.authenticate(email, password)

		if not user:
			flash("Invalid credentials.", 'red')
			return redirect(url_for('login'))	

		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)

	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

##############################################################################
# User routes

# @app.route('/user/<username>')
# @login_required
# def user(username):
# 	""" Show user dashboard with three searches thumbnails """

# 	if username != current_user.username:
# 		return redirect('/')
	
# 	return render_template('user.html', user=user)

# @app.route('/users/<username>/profile', methods=['GET', 'POST'])
# @login_required
# def user_profile(username):
# 	""" Show user profile page with edit form """

# @app.route('/users/<username>/searches')
# @login_required
# def user_searches(username)
# 	""" Show user's searches thumbnails """

# @app.route('/users/<username>/delete', methods=['POST'])
# @login_required
# def delete_user(username)
# 	""" Delete user """

	# Password required for this

##############################################################################
# Searches

@app.route('/searches', methods=['GET', 'POST'])
def searches():

	search = session.get('search')

	return render_template('search.html', search=search)


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





