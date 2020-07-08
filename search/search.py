from flask import Blueprint, render_template, redirect, request, url_for, jsonify, session, flash
from flask_login import login_required, current_user

from forms import SearchForm
from models import Search, db, User
from helper import get_covid_data, get_state_and_county, serialize
from datetime import datetime

import requests
import wtforms_json

wtforms_json.init()

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['POST'])
def search():
	form = SearchForm.from_json(request.get_json(), csrf_enabled=False)

	if form.validate():
    # Get state and county from location
		location = get_state_and_county(form.location.data)
    
		# If answer is not a dict with results, return error message.
		if type(location) != dict:
			return 'invalid location'

    # Turn date object into string
		date = str(form.date.data)
		
		county = location['county'].lower()
		state = location['state'].lower()

    # Get cases and deaths for selected dates
		covid_data = get_covid_data(date, state, county)

		if type(covid_data) != dict:
			return covid_data

		return jsonify(covid_data)
		
	return 'invalid request'

	""" Show search or search result """

@search_bp.route('/search/save', methods=['POST'])
def save_search():
	""" If user is logged in, save search to user, else save to 
	session and redirect user to login 
	"""

	if current_user.is_authenticated:
		s = Search.create(request.json)
		current_user.searches.append(s)
		db.session.commit()
		return 'saved'
	else:
		session['search'] = serialize(request.json)
		return 'login'

@search_bp.route('/search/load', methods=['GET'])
@login_required
def load_search():

	search_id = request.args.get('id')

	s = Search.query.get_or_404(search_id)

	s.deaths = s.deaths.split(',')
	s.dates = s.dates.split(',')
	s.cases = s.cases.split(',')

	return jsonify(s.serialize())

@search_bp.route('/search/<int:search_id>/delete', methods=['POST'])
@login_required
def delete_search(search_id):
	"""Delete saved search"""
		
	s = Search.query.get_or_404(search_id) 
	if current_user.id != s.user_id:
		flash('Access unathorized', 'danger')
		return redirect(url_for('index'))
		
	db.session.delete(s)
	db.session.commit()

	return 'deleted'
