#! .\.venv\scripts\python.exe

import geocoder
import requests

def search_for_nearby_establishment(lat, lng, radius, establishment, api_key):
    places_base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{lat},{lng}',
        'radius': radius,
        'keyword': establishment,
        'type': 'restaurant',
        'key': api_key
    }
    response = requests.get(places_base_url, params=params)
    data = response.json()
    return data['results']

def text_serach(query, radius, api_key):
    places_base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'location': f'{lat},{lng}',
        'radius': radius,
        'type': 'restaurant',
        'key': api_key
    }
    response = requests.get(places_base_url, params=params)
    data = response.json()
    return data['results']
    

# Google Places API
user_loc = geocoder.ip('me')
lat, lng = user_loc.latlng
places_api_key = "AIzaSyBrIR_uTrPSrJ0QcmkWHo1tiT42X1CPudU"

fast_food = ["MCDONALD'S", "SUBWAY", "TACO BELL", "CHICK-FIL-A", "WENDY'S", "BURGER KING", "DOMINO'S", "PIZZA HUT", "CHIPOTLE", "SONIC DRIVE-IN"]

# results = []
# for establishment in fast_food:
#     results.extend(search_for_nearby_establishment(lat, lng, 5000, establishment, places_api_key))
    
results = text_serach('fast food', 5000, places_api_key)

# Extract relevant information from API response
print(len(results))
print(results[0])
locations = [(result["name"], result["formatted_address"], result["geometry"]["location"]) for result in results]
restaurant_names = {result["name"] for result in results}
# print(locations)
print(restaurant_names, len(restaurant_names))


"""
 What we want to do next
 - Make a list of all the unique establishmet names
    - May want to check for weird duplicates like the chik-fila one
 - Feed those establishment names into Nutritionix API and get all the menu items and nutrition info
 - Filter the menu items down to meals
 - Create a dataframe with the name of the menu item and all the relevant nutirional information and the nearest store location
 - Create a column which assigns each a score form 1 to 10
 - Create a funtion which returns a list of meals, filtered by their score and ordered closest to farthest from user location
"""
# print(results)
# print(locations)

# # Print out names and addresses of nearby fast food locations
# for name, address in locations:
#     print(f"{name}: {address}")


