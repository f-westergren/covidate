from flask import redirect, render_template, url_for, request, flash
from werkzeug.urls import url_parse

from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from app.forms import LoginForm
from app.models import User, Search

from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

##############################################################################
# Login and logout routes

@app.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('show_dashboard'))
	
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
			next_page = url_for('show_dashboard')
		return redirect(next_page)


		
	
	return render_template('login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def show_dashboard():
	user = current_user
	return render_template('dashboard.html', user=user)