#! .\.venv\scripts\python.exe

import geocoder
import requests

user_loc = geocoder.ip('me')

# Google Places API
places_api_key = "AIzaSyBrIR_uTrPSrJ0QcmkWHo1tiT42X1CPudU"
places_base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

lat, lng = user_loc.latlng
# Set up parameters for API request
lat_lng = f"{lat},{lng}"  # Example latitude and longitude
search_radius = "50000"  # Search radius in meters
place_type = "restaurant"  # Type of place to search for
# keyword = "(mcdonald) OR (wendy)"  # Keyword to search for

# Construct URL for API request
# url = f"{places_base_url}?location={lat_lng}&radius={search_radius}&type={place_type}&keyword={keyword}&key={places_api_key}"
# url = f"{places_base_url}?location={lat_lng}&radius={search_radius}&key={places_api_key}"

# # Send API request and get response
# response = requests.get(url)
# data = response.json()

def get_nearby_places(lat, lng, radius, type_, api_key):
    endpoint_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    places = []
    next_page_token = None
    
    while True:
        params = {
            'location': f'{lat},{lng}',
            'radius': radius,
            'type': type_,
            'key': api_key
        }
        if next_page_token:
            params['pagetoken'] = next_page_token
        response = requests.get(endpoint_url, params=params)
        data = response.json()
        places.extend(data['results'])
        next_page_token = data.get('next_page_token')
        if not next_page_token:
            break
    return places

from bs4 import BeautifulSoup

def get_fast_food_nearby(lat, lng):
    url = f'https://www.google.com/maps/search/fast+food/@{lat},{lng},14z/data=!3m1!4b1'
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    results = soup.find_all('div')
    print(results)
    return results

places = get_fast_food_nearby(lat, lng)
print(places)
results = get_nearby_places(lat, lng, search_radius, place_type, places_api_key)

# Extract relevant information from API response
# results = data["results"]
print(len(results))
locations = [(result["name"], result["vicinity"], result["geometry"]["location"]) for result in results]
restaurant_names = {result["name"] for result in results}
print(restaurant_names, len(restaurant_names))

fast_food = ["MCDONALD'S", "SUBWAY", "TACO BELL", "CHICK-FIL-A", "WENDY'S", "BURGER KING", "DOMINO'S", "PANERA BREAD", "PIZZA HUT", "CHIPOTLE", "SONIC DRIVE-IN"]

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


