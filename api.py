#! .\.venv\scripts\python.exe
from constants import PLACES_API_KEY

import geocoder
import requests

def get_current_location():
    """Get latitude and longitide of the current IP address

  Returns:
      floats: lat, lng
  """
    user_loc = geocoder.ip('me')
    lat, lng = user_loc.latlng
    return lat, lng

def get_lat_lng_from_string():
    pass

def find_fast_food_near(lat, lng, query, radius):
    places_base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'location': f'{lat},{lng}',
        'radius': radius,
        'type': 'restaurant',
        'key': PLACES_API_KEY
    }
    response = requests.get(places_base_url, params=params)
    data = response.json()
    results = data['results']
    return [(result["name"], result["formatted_address"], result["geometry"]["location"]) for result in results]
    
def get_cheat_meals(current_location=True, location_string='', query='fast food', radius=5000):
    if (current_location):
        lat, lng = get_current_location()
    else:
        lat, lng = get_lat_lng_from_string(location_string)
    fast_food_lcoations = find_fast_food_near(lat, lng, query, radius)
    print(fast_food_lcoations)


if __name__ == "__main__":
    get_cheat_meals()