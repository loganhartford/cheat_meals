#! .\.venv\scripts\python.exe
from constants import *
import geocoder
import requests
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import pgeocode

# For Dev only
# pd.set_option('display.max_columns', None)

def get_coordinates_from_address(address):
    geocoder_base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": PLACES_API_KEY
    }
    response = requests.get(geocoder_base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        return data['status']
    

# def get_coordinates(country_code, postal_code):
#     nomi = pgeocode.Nominatim(country_code)
#     location = nomi.query_postal_code(postal_code)
#     return location.latitude, location.longitude

def find_restaurants_near(lat, lng, query, radius):
    """Returns a list of restaurants withing the radius of the location which match the search query.

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
        "query": query,
        "location": f'{lat},{lng}',
        "radius": radius,
        "type": "restaurant",
        "key": PLACES_API_KEY
    }
    response = requests.get(places_base_url, params=params)
    data = response.json()
    if data['status'] == 'OK':
        results = data['results']
        return [(result["name"], result["formatted_address"], result["geometry"]["location"]["lat"], result["geometry"]["location"]["lng"]) for result in results]
    else:
        return data['status']
    
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

def clean_restaurant_name(restaurant_locations_df):
    # remove appostrophes and set to lowercase
    return restaurant_locations_df.apply(lambda df: df["Name"].replace("'", "").lower(), axis=1)

def get_restaurant_nutrition_data(restaurant_locations_df):
    restaurant_names = restaurant_locations_df["Name"].values.tolist()
    
    # Using a local dataset for now, will make a db later
    nutrition_df = pd.read_csv("fastfood.csv")
    meal_items_df = nutrition_df[nutrition_df["restaurant"].str.lower().isin(restaurant_names)]

    # Anything less than 500 cals is probably not a cheat meal
    meal_items_df = meal_items_df[meal_items_df["calories"] > 500]
    meal_items_df["restaurant"] = meal_items_df["restaurant"].str.lower()
    return meal_items_df  

def get_linear_constants(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    m = (y2 - y1)/(x2 - x1)
    b = y1 - m*x1
    return m , b

def calculate_cheat_score(total_cals, total_fat, sodium, sugar):
    # Calories
    m, b = get_linear_constants((CALORIE_MIN, 0), (CALORIE_MAX, CALORIE_WEIGHT))
    calorie_score = m*total_cals + b
    # Fat %
    m, b = get_linear_constants((PERCENT_FAT_MIN, 0), (PERCENT_FAT_MAX, 2))
    fat_score = min(m*total_fat*9/total_cals + b, 3)
    # Sodium
    sodium_score = min(sodium/SODIUM_RDA, 2)
    # Sugar
    sugar_score = min(sugar/SUGAR_RDA, 4)

    cheat_score = round(min(calorie_score + fat_score + sodium_score + sugar_score, 10), 2)

    return cheat_score
    
def create_cheat_score_column(meal_items_df):
    # Calculate and add cheat score to the df
    return meal_items_df.apply(lambda df: calculate_cheat_score(df["calories"], df["total_fat"], df["sodium"], df["sugar"]), axis=1)

def remove_restaurants_without_meals(meal_items_df, restaurant_locations_df):
    restaurants = meal_items_df["restaurant"].unique()
    return restaurant_locations_df[restaurant_locations_df["Name"].isin(restaurants)].reset_index(drop=True)

def get_distance(restaurant_name, restaurant_locations_df):
    df = restaurant_locations_df
    return df.loc[df["Name"]==restaurant_name]["Distance in Km"].values[0]

def get_address(restaurant_name, restaurant_locations_df):
    df = restaurant_locations_df
    return df.loc[df["Name"]==restaurant_name]["Address"].values[0]


def create_distance_and_location_column(meal_items_df, restaurant_locations_df):
    address_col = meal_items_df.apply(lambda df: get_address(df["restaurant"], restaurant_locations_df), axis=1).values.tolist()
    distance_col = meal_items_df.apply(lambda df: get_distance(df["restaurant"], restaurant_locations_df), axis=1).values.tolist()
    return address_col, distance_col


def get_cheat_meals(address="68 hall avenue guelph on", query='fast food', radius=5000, cheat_score_target=7.5):
    # Get the search area coordinates
    lat, lng = get_coordinates_from_address(address)
    
    # Get the locations from Places API
    restuarant_locations = find_restaurants_near(lat, lng, query, radius)

    # Create the locations df
    rest_locs_df = convert_locations_to_df(restuarant_locations)
    rest_locs_df = add_distance_to_df(rest_locs_df, lat, lng)
    rest_locs_df = keep_only_closest_location(rest_locs_df)
    rest_locs_df["Name"] = clean_restaurant_name(rest_locs_df)
    print(rest_locs_df)

    # Create the menu items df from nearby locations
    menu_items_df = get_restaurant_nutrition_data(rest_locs_df)

    # Add additional informationt to the menu items
    menu_items_df["cheat_score"] = create_cheat_score_column(menu_items_df)
    rest_locs_df = remove_restaurants_without_meals(menu_items_df, rest_locs_df)
    menu_items_df["address"], menu_items_df["distance in km"] = create_distance_and_location_column(menu_items_df, rest_locs_df)

    # Filter and sort based on target cheat score
    mask1 = menu_items_df["cheat_score"] > (cheat_score_target - 1)
    mask2 = menu_items_df["cheat_score"] < (cheat_score_target + 1)
    cheat_meals_df = menu_items_df[mask1 & mask2]
    cheat_meals_df["score_delta"] = abs(cheat_meals_df["cheat_score"] - cheat_score_target)
    cheat_meals_df = cheat_meals_df.sort_values(by=["score_delta", "distance in km"]).reset_index(drop=True)

    return cheat_meals_df

    
    
    
    


if __name__ == "__main__":
    get_cheat_meals()
    # get_restaurant_nutrition_data()
    # calculate_cheat_score(2500, 50, 4000, 50)