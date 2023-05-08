#! .\.venv\scripts\python.exe
from constants import *
import geocoder
import requests
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import pgeocode

# For Dev only
# pd.set_option('display.max_columns', None)

def get_coordinates(country_code, postal_code):
    nomi = pgeocode.Nominatim(country_code)
    location = nomi.query_postal_code(postal_code)
    print(location.latitude, location.longitude)
    return location.latitude, location.longitude

def find_restaurants_near(lat, lng, query, radius):
    """Returns a list of restaurants withing the radius of the location whihc match the search query.

    Args:
        lat (float): Latitiude of search location
        lng (float): Longitude of search location
        query (String): Type of restaurant
        radius (int): Search radius around location

    Returns:
        list: list of tuples, with each tupe being a restaurant location
    """
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
    return [(result["name"], result["formatted_address"], result["geometry"]["location"]["lat"], result["geometry"]["location"]["lng"]) for result in results]
    
def convert_locations_to_df(locations_list):
    """Convert a list of fast-food locations into a DataFram

    Args:
        locations_list (list): list of tuples with each tuple being a fast food locations

    Returns:
        DataFrame: Contains all the fastfood locations
    """
    columns = ["Name", "Address", "Latitude", "Longitude"]
    return pd.DataFrame(locations_list, columns=columns)

def find_distance_between_coordinates(lat1, lng1, lat2, lng2):
    lat1_r = radians(lat1)
    lng1_r = radians(lng1)
    lat2_r = radians(lat2)
    lng2_r = radians(lng2)

    dlon = lng2_r - lng1_r
    dlat = lat2_r - lat1_r

    a = sin(dlat / 2)**2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return RADIUS_OF_EARTH_IN_KM * c

def add_distance_to_df(restaurant_locations_df, lat, lng):
    restaurant_locations_df["Distance in Km"] = restaurant_locations_df.apply(lambda df: find_distance_between_coordinates(lat, lng, df["Latitude"], df["Longitude"]), axis=1)
    return restaurant_locations_df.sort_values(by=["Distance in Km"])
    
def keep_only_closest_location(restaurant_locations_df):
    return restaurant_locations_df.drop_duplicates(subset=["Name"], keep="first").reset_index(drop=True)

def get_restaurant_nutrition_data(restaurant_locations_df):
    restaurant_names = restaurant_locations_df["Name"].values.tolist()
    # Remove apostrophes since they aren't used in the dataset
    restaurant_names = [name.replace("'", "") for name in restaurant_names]
    
    # Using a local dataset for now, will make a db later
    nutrition_df = pd.read_csv("fastfood.csv")
    meal_items_df = nutrition_df[nutrition_df["restaurant"].isin(restaurant_names)]
    # Anything less than 500 cals is probably not a cheat meal
    meal_items_df = meal_items_df[meal_items_df["calories"] < 500]
    meal_items_df.to_csv("sub5.csv")
    print(meal_items_df)

def calculate_cheat_score(total_cals, total_fat, sodium, sugar):
    pass
    # Each item maps from min to max linearly from 0 to the max weight
    # Don't care if it goes over, max score is capped at 10
    

def get_cheat_meals(country_code='us', postal_code='78653', query='fast food', radius=5000):
    # Get the search area coordinates
    lat, lng = get_coordinates(country_code, postal_code)
    
    # Get the locations from Places API
    restuarant_locations = find_restaurants_near(lat, lng, query, radius)

    # Create the locations df
    rest_locs_df = convert_locations_to_df(restuarant_locations)
    rest_locs_df = add_distance_to_df(rest_locs_df, lat, lng)
    rest_locs_df = keep_only_closest_location(rest_locs_df)

    get_restaurant_nutrition_data(rest_locs_df)

    print(rest_locs_df)
    
    
    


if __name__ == "__main__":
    # print(get_coordinates('us', '78653'))
    get_cheat_meals()
    # get_restaurant_nutrition_data()