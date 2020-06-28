from flask import Blueprint, session, jsonify
from flask_cors import cross_origin, CORS
import wtforms_json

from app.forms import SearchForm
from app.helper import get_state_and_county, get_covid_data

cors = CORS(app, resources={r'/search': {"origins": "*"}})
wtforms_json.init()


@search_bp.route('/search', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type','Authorization'])
def search():
	
	form = SearchForm.from_json(request.get_json(), csrf_enabled=False)

	# TODO: Make sure date is not before today's date.

	if form.validate():
		location = get_state_and_county(form.location.data)
		date = str(form.date.data)
		
		county = location['county'].lower()
		state = location['state'].lower()

		covid_data = get_covid_data(date, state, county)

		return jsonify(covid_data)
		


	return 'Nope!'