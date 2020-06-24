from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, current_user, login_user

from models import db, connect_db, User, Search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///covid-event-search'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
login = LoginManager(app)

@app.route('/')
def index():
	return render_template("index.html")

##############################################################################
# Login route

@app.route('/login', methods=['GET, POST'])
def login():

	if current_user.is_authenticated:
		return redirect(url_for('index'))
	
	form = LoginForm()

	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = User.authenticate(email, password)
		
		if user:
			flash(f'Welcome back, {user.name}!', 'success')
			login_user(user, remember=form.remember_me.data)
			return redirect_for('index')
	
	return render_template('login.html', title='Sign In', form=form)