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
# Login and logout routes

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





