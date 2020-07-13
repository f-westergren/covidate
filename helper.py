import os
import requests
from states import states
from datetime import datetime
from models import db, Search, User

BASE_MAP_API_URL = 'http://www.mapquestapi.com/geocoding/v1'
BASE_COVID_API_URL = 'https://corona.lmao.ninja/v2/historical/usacounties'

MAPQUEST_API_KEY = os.environ.get('MAPQUEST_API')

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

  # If country not USA
  if country != 'US':
    return 'not usa'

  # If no county
  if county == '':
    return "no county"

  # Strip 'County/Parish' from county name (except DC)
  if ' ' in county and county != "District of Columbia":
    county_name = county[0:county.rindex(' ')]
  
  else:
    county_name = county

  return {'state': states[state], 'county': county_name}

def get_covid_data(date, state, county):
  """ Get data from COVID-api and return array of dates with data"""

  date = datetime.strptime(date, '%Y-%m-%d')
  diff = datetime.now() - date
  days = diff.days

  if days < 2:
    return 'invalid date'
  res = requests.get(f'{BASE_COVID_API_URL}/{state}', params={'lastdays': days})

  for c in res.json():
    if c['county'] == county:
      timeline = c['timeline']
      dates = [date.replace('/', '-') for date in timeline['cases']]
      cases = [timeline['cases'][num] for num in timeline['cases']]
      deaths = [timeline['deaths'][num] for num in timeline['deaths']]
      change_cases = [y - x for x, y in zip(cases, cases[1:])]
      change_cases.insert(0, None)
      change_deaths = [y - x for x, y in zip(deaths, deaths[1:])]
      change_deaths.insert(0, None)
      return {
        'dates': dates, 
        'cases': cases, 
        'deaths': deaths, 
        'change_cases': change_cases, 
        'change_deaths': change_deaths
      }

  return 'no data'

def serialize(obj):
  dict = {}
  for key, value in obj.items():
    dict[key] = value
  return dict