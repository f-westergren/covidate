from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin, CORS

from forms import SearchForm
from models import Search
from helper import get_covid_data, get_state_and_county

import requests
import wtforms_json

wtforms_json.init()

search_bp = Blueprint('search_bp', __name__,
  template_folder='templates',
  static_folder='static'
)

cors = CORS(search_bp, resources={r'/search': {"origins": "*"}})

@search_bp.route('/search', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def search():
	
	form = SearchForm.from_json(request.get_json(), csrf_enabled=False)

	# TODO: Make sure date is not before today's date.

	if form.validate():
    # Get state and county from location
		location = get_state_and_county(form.location.data)
    
    # Turn date object into string
		date = str(form.date.data)
		
		county = location['county'].lower()
		state = location['state'].lower()

    # Get cases and deaths for selected dates
		covid_data = get_covid_data(date, state, county)

		return jsonify(covid_data)
		


	return 'Nope!'

	""" Show search or search result """

	# Option to create account and save search?
	# If logged in, option to save search

# @app.route('/searches/<int:search_id>', methods=['GET', 'POST'])
# @login_required
# def search(search_id):
# 	""" Show and edit search """																

# @app.route('searches/<int:search_id>/delete')
# @login_required
# 	def delete_search(search_id):
# 		"""Delete saved search"""