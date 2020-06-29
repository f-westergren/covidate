from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from models import User

user_bp = Blueprint('user_bp', __name__,
  template_folder='templates',
  static_folder='static'
)


# @app.route('/user/<username>')
# @login_required
# def user(username):
# 	""" Show user dashboard with three searches thumbnails """

# 	if username != current_user.username:
# 		return redirect('/')
	
# 	return render_template('user.html', user=user)

# @app.route('/user/<username>/profile', methods=['GET', 'POST'])
# @login_required
# def user_profile(username):
# 	""" Show user profile page with edit form """

@user_bp.route('/user/<username>/searches')
@login_required
def searches(username):
	""" Show user's searches thumbnails """
	

	return render_template('/user/searches.html')

# @app.route('/user/<username>/delete', methods=['POST'])
# @login_required
# def delete_user(username)
# 	""" Delete user """

	# Password required for this