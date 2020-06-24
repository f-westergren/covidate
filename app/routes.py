from flask import redirect, render_template, url_for, request, flash
from werkzeug.urls import url_parse

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from app.forms import LoginForm
from app.models import User, Search

from app import app

@app.route('/')
def index():

	return render_template("index.html", user=current_user)

##############################################################################
# Login, logout and register routes

@app.route('/login', methods=['GET', 'POST'])
def login():

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
	return redirect(url_for('/'))

##############################################################################
# User routes

@app.route('/user/<int:user_id>')
@login_required
def user(user_id):
	user = current_user

	if user_id != user.id:
		return redirect('/')
	
	return render_template('user.html', user=user)

# @app.route('/users/<int:user_id>/profile', methods=['GET', 'POST'])

	# View and edit profile

# @app.route('/users/<int:user_id>/searches')

	# View all user's searches

##############################################################################
# Searches

# @app.route('/searches', methods=['GET', 'POST'])

	# View and create search
	# Option to create account and save search?
	# If logged in, option to save search

# @app.route('searches/<int:search_id>', methods=['GET', 'POST'])
# @login_required

	# View and edit saved searches

# @app.route('searches/<int:search_id>/delete')
# @login_required

	# Delete saved search





