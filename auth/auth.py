from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_login import login_required, logout_user, current_user, login_user
from werkzeug.urls import url_parse
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, SignupForm
from models import User, db, Search

auth_bp = Blueprint('auth_bp', __name__,
  template_folder='templates',
  static_folder='static'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	""" Show login page with login form """

	# If user has been redirected to save a search, show flash message.
	if request.args.get('saveSearch') and request.method == 'GET':
		flash('Please log in to save search.', 'success')

	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()

	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.authenticate(username, password)

		if user:
			login_user(user)
		
		# If user has saved search in session, save it to database and delete session.
			if 'search' in session:
				s = Search.create(session['search'])
				user.searches.append(s)
				db.session.commit()
				del session['search']
				flash("Search saved", 'success')
				return redirect(f'/user/{user.username}/searches')

			return redirect(url_for('index'))

		flash("Invalid credentials.", 'danger')
		
	return render_template('/login.html', form=form, btnText="Log in", cancel='index', color="#F5DDDD")

@auth_bp.route('/signup', methods=['GET', 'POST'])
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
			return redirect(url_for('auth_bp.signup'))
		
		login_user(user)
		return redirect(url_for('index'))
	
	return render_template('signup.html', form=form, btnText="Sign Up", cancel='index', color="#F5DDDD")

@auth_bp.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))