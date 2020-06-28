import os
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from sqlalchemy.exc import IntegrityError
from app.forms import LoginForm, SignupForm

from app.models import User


#Blueprint Configuration
auth_bp = Blueprint(
	'auth_bp', __name__,
	template_folder='templates',
	static_folder='static'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	""" Show login page with login form """
	print("OS FROM AUTH", os.environ.get('DATABASE_URL'))
	if current_user.is_authenticated:
		return redirect(url_for('/'))
	
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.authenticate(username, password)

		if not user:
			flash("Invalid credentials.", 'danger')
			return redirect(url_for('auth_bp.login'))	

		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index_bp.index')
		return redirect(next_page)

	return render_template('/user/login.html', form=form)

@auth_bp.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index_bp.index'))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	"""Handle user signup.

  Create new user and add to DB. Redirect to home page.

  If form not valid, present form.

  If the there already is a user with that username: flash message
  and re-present form.
  """

	if current_user.is_authenticated:
		return redirect(url_for('index_bp.index'))

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
		return redirect(url_for('index_bp.index'))
	
	return render_template('user/signup.html', form=form)