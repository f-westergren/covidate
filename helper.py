import requests
from secrets import MAPQUEST_API_KEY
from states import states
from datetime import datetime
from models import db, Search, User

BASE_MAP_API_URL = 'http://www.mapquestapi.com/geocoding/v1'
BASE_COVID_API_URL = 'https://corona.lmao.ninja/v2/historical/usacounties'

def get_state_and_county(location):
  """ Get locations from api from input location"""

  # Right now this will only return the first result, add functionality for this.
  try:
    res = requests.get(f'{BASE_MAP_API_URL}/address', 
    params={'key': MAPQUEST_API_KEY, 'location': location})
  except Error:
    return Error

  data = res.json()['results'][0]['locations'][0]

  # Check to see if country is US, if so, add to locations.
  country = data['adminArea1']
  state = data['adminArea3']
  county = data['adminArea4']

  # Strip 'County' from county name
  county_name = county[0:-7] if county[-6:] == 'County' else county

  # Only return if location is in US.
  if country == 'US' and data['geocodeQuality'] != 'COUNTRY':
    return {'state': states[state], 'county': county_name}

  # Otherwise return error string.
  return "Can't find location in USA."
    

def get_covid_data(date, state, county):
  """ Get data from COVID-api and return array of dates with data"""

  date = datetime.strptime(date, '%Y-%m-%d')
  diff = datetime.now() - date
  days = diff.days

  res = requests.get(f'{BASE_COVID_API_URL}/{state}', params={'lastdays': days})

  for c in res.json():
    if c['county'] == county:
      timeline = c['timeline']
      dates = [date.replace('/', '-') for date in timeline['cases']]
      cases = [timeline['cases'][num] for num in timeline['cases']]
      deaths = [timeline['deaths'][num] for num in timeline['deaths']]

      return {'dates': dates, 'cases': cases, 'deaths': deaths}

  return res

def save_new_search(data, user=False):
  # Change this to use current_user
  if user:
    location, date, dates, cases, deaths, user_id = data.values()
  else: 
    location, date, dates, cases, deaths = data.values()
  s = Search(
	  location=location,
	  date=date, 
	  dates=dates, 
	  cases=cases,
	  deaths=deaths, 
	  created_at=datetime.now().strftime("%m/%d/%Y"),
	  description = f'Cases from {date} in {location}', #TODO: Make sure this is in American format
	)
  if user:
    user.searches.append(search)
    db.session.commit()
  
  else:
    return s.serialize()


  # Error handling for no county
  # Error handling for no state
  # Error handling for no data?
  


# Räkna ut dagar att requesta
  # dagens datum minuns requestat datum
  # det här blir parameter lastdays

# Requesta med stat som stat och lastdays som lastsdays

# Ta ut resultat beroende på vilket county.

# Lägg resultatet med datumen i en array?

