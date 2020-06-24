from flask import redirect, render_template
from flask_login import LoginManager, current_user, login_user

from app.forms import LoginForm

from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

##############################################################################
# Login route

@app.route('/login', methods=['GET', 'POST'])
def user_login():

	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = User.authenticate(email, password)
		
		if user:
			login_user(user, remember=form.remember_me.data)
			return redirect_for('index')

		flash("Invalid credentials.", 'danger')
	
	return render_template('login.html', form=form)

	@app.route('/dashboard')
	def show_dashboard():

		return render_template('dashboard.html', user=user)