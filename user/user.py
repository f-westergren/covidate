from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from forms import EditPasswordForm, EditUserForm
from flask_bcrypt import Bcrypt

from models import User, db

user_bp = Blueprint('user_bp', __name__,
  template_folder='templates',
  static_folder='static'
)

bcrypt = Bcrypt()

# @app.route('/user/<username>')
# @login_required
# def user(username):
# 	""" Show user dashboard with three searches thumbnails """

# 	if username != current_user.username:
# 		return redirect('/')
	
# 	return render_template('user.html', user=user)

@user_bp.route('/user/<username>/profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
	""" Show Edit User Profile Form """

	#TODO: Check why username is still taken when changed

	if current_user.username != username:
		flash('Access unathorized', 'danger')
		return redirect(url_for('index'))

	user = current_user

	form = EditUserForm(obj=user)

	if form.validate_on_submit():
		user = User.authenticate(current_user.username, form.password.data)

		if user:
			user.username = form.username.data
			user.email = form.email.data
			db.session.commit()
			flash('User information updated', 'success')
			return redirect(url_for('index'))

		flash('Invalid credentials.', 'danger')
  
	return render_template('profile.html', form=form)

@user_bp.route('/user/<username>/password', methods=['GET', 'POST'])
@login_required
def edit_password(username):

	if current_user.username != username:
		flash('Access unathorized', 'danger')
		return redirect(url_for('index'))
	
	user = current_user

	form = EditPasswordForm(obj=user)
	
	if form.validate_on_submit():
		user = User.authenticate(user.username, form.current_password.data)

		if user:
			# Hash new password before updating user.password
			hashed_pwd = bcrypt.generate_password_hash(form.new_password.data).decode('UTF-8')
			user.password = hashed_pwd
			db.session.commit()
			flash('Password updated!', 'success')
			return redirect(url_for('user_bp.edit_profile', username=current_user.username))

		flash('Incorrect password.', 'danger')

	return render_template('password.html', form=form, btnText='Submit', cancel='user_bp.edit_profile')

@user_bp.route('/user/<username>/searches')
@login_required
def searches(username):
	""" Show user's searches thumbnails """
	

	return render_template('/searches.html')

# @app.route('/user/<username>/delete', methods=['POST'])
# @login_required
# def delete_user(username)
# 	""" Delete user """

	# Password required for this
