from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from forms import EditPasswordForm, EditUserForm
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import InvalidRequestError, IntegrityError

from models import User, db

user_bp = Blueprint('user_bp', __name__,
  template_folder='templates',
  static_folder='user-static'
)

bcrypt = Bcrypt()

@user_bp.route('/user/<username>/profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
	""" Show Edit User Profile Form """

	if current_user.username != username:
		flash('Access unathorized', 'danger')
		return redirect(url_for('index'))

	user = current_user

	form = EditUserForm(obj=user)

	if form.validate_on_submit():
		user = User.authenticate(current_user.username, form.password.data)

		if user:
			try:
				user.username = form.username.data
				user.email = form.email.data
				db.session.commit()
				flash('User information updated', 'success')
				return redirect(url_for('index'))

			except:
				db.session.rollback()
				flash('Username taken.', 'danger')
		else:
			flash('Invalid credentials.', 'danger')
  
	return render_template('profile.html', 
		form=form, 
		btnText='Submit', 
		cancel='index', 
		color="#ACDAAA"
	)

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
			return redirect(url_for('user_bp.edit_profile', username=user.username))

		flash('Incorrect password.', 'danger')

	return render_template('password.html', 
		form=form, 
		btnText='Submit', 
		cancel='user_bp.edit_profile', 
		color="#FFF199"
	)

@user_bp.route('/user/<username>/searches')
@login_required
def searches(username):
	""" Show user's searches thumbnails """
	
	return render_template('/searches.html', user=current_user, color="#FFF199")

@user_bp.route('/user/<username>/delete', methods=['POST'])
@login_required
def delete_user(username):
	""" Delete user """

	if current_user.username != username:
		flash('Access unathorized', 'danger')
		return redirect(url_for('index'))

	logout_user()
	db.session.delete(current_user)
	db.session.commit()

	return redirect(url_for('auth_bp.signup'))