import requests
from app.secrets import MAPQUEST_API_KEY
from app.states import states

BASE_MAP_API_URL = 'http://www.mapquestapi.com/geocoding/v1'

def get_state_and_county(location):
  """ Get locations from api from input location"""

  # Right now this will only return the first result, add functionality for this.
  try:
    res = requests.get(f'{BASE_MAP_API_URL}/address', 
    params={'key': MAPQUEST_API_KEY, 'location': location})
  except Error:
    return Error

  data = res.json()['results'][0]

  locations = []

  # Check to see if country is US, if so, add to locations.
  for place in data['locations']:
    country = place['adminArea1']

    if country == 'US' and place['geocodeQuality'] != 'COUNTRY':
      state = place['adminArea3']
      county = place['adminArea4']

      # Strip 'County' from county name
      county_name = county[0:-7] if county[-6:] == 'County' else county

      # Only add if result exists and change state code to name.
      if state != '' and county_name != '':
        locations.append({'state': states[state], 'county': county_name})
  
  # If no location, return error.
  if len(locations) == 0:
    return "Can't find location in USA."

  return locations