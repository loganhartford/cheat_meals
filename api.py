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
    """Get gps coordinates from and address using google's geocoding api"

    Args:
        address (String): "<street address> <city> <province/state>"

    Returns:
        floats or String: returns the lat and lng or status code if there was a problem
    """
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
    """Convert a list of fast-food locations into a DataFrame

    Args:
        locations_list (list): list of tuples with each tuple being a fast food locations

    Returns:
        DataFrame: Contains all the fastfood locations
    """
    columns = ["Name", "Address", "Latitude", "Longitude"]
    return pd.DataFrame(locations_list, columns=columns)

def find_distance_between_coordinates(lat1, lng1, lat2, lng2):
    """Find the distance in Km between a set of gps coordinates

    Args:
        lat1 (flaot): latitude coordinate
        lng1 (flaot): longitude coordinate
        lat2 (flaot): latitude coordinate
        lng2 (flaot): longitude coordinate

    Returns:
        float: distance between sets of coordinates
    """
    lat1_r = radians(lat1)
    lng1_r = radians(lng1)
    lat2_r = radians(lat2)
    lng2_r = radians(lng2)

    dlon = lng2_r - lng1_r
    dlat = lat2_r - lat1_r

    a = sin(dlat / 2)**2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return RADIUS_OF_EARTH_IN_KM * c

def generate_distance_col(restaurant_locations_df, lat, lng):
    # Calculate the distance from address to restaurants
    return restaurant_locations_df.apply(lambda df: find_distance_between_coordinates(lat, lng, df["Latitude"], df["Longitude"]), axis=1)
    
def keep_only_closest_location(restaurant_locations_df):
    # Only care about the closest location for each chain
    return restaurant_locations_df.drop_duplicates(subset=["Name"], keep="first").reset_index(drop=True)

def clean_restaurant_name(restaurant_locations_df):
    # Remove appostrophes and set to lowercase
    return restaurant_locations_df.apply(lambda df: df["Name"].replace("'", "").lower(), axis=1)

def create_locations_df(lat, lng, query, radius):
    """Create a DataFrame containing all of the restaurant location matching the query within the radius of the gps coordinates

    Args:
        lat (float): Latitude coordinate
        lng (float): Longitude coordinate
        query (String): Restaurant type
        radius (int): Radius around coordinates to search

    Returns:
        pandas.DataFrame: Contains all of the restaurant location within the radius
    """
    # Get the locations from Places API
    restuarant_locations = find_restaurants_near(lat, lng, query, radius)

    df = convert_locations_to_df(restuarant_locations)
    df["Distance in Km"] = generate_distance_col(df, lat, lng)
    df.sort_values(by=["Distance in Km"])
    df = keep_only_closest_location(df)
    df["Name"] = clean_restaurant_name(df)
    return df

def get_restaurant_nutrition_data(restaurant_locations_df):
    """Get available menu items from the fastfood data set and do some simple filtering

    Args:
        restaurant_locations_df (pandas.DataFram): Contains nearby restaurant locations

    Returns:
        pandas.DataFrame: Contains meal items from nearby restaurant locations
    """
    restaurant_names = restaurant_locations_df["Name"].values.tolist()
    
    # Using a local dataset for now, will make a db later
    nutrition_df = pd.read_csv("fastfood.csv")
    meal_items_df = nutrition_df[nutrition_df["restaurant"].str.lower().isin(restaurant_names)]

    # Anything less than 500 cals is probably not a cheat meal
    meal_items_df = meal_items_df[meal_items_df["calories"] > 500]
    meal_items_df["restaurant"] = meal_items_df["restaurant"].str.lower()
    return meal_items_df  

def get_linear_constants(point1, point2):
    """Return the slope and y-intercept for a line based on two x and y coordinates

    Args:
        point1 (tuple): (x, y)
        point2 (tuple): (x, y)

    Returns:
        float, float: slope, y-intercept
    """
    x1, y1 = point1
    x2, y2 = point2
    m = (y2 - y1)/(x2 - x1)
    b = y1 - m*x1
    return m , b

def calculate_cheat_score(total_cals, total_fat, sodium, sugar):
    """Quantifies how unhealthy or indulgent a food item is based on calories, % of calories from fat, sodium and sugar

    Args:
        total_cals (float): Total food item calories
        total_fat (float): Total food item grams of fat
        sodium (float): Total food item sodium in mg
        sugar (float): Total food item sugar in g

    Returns:
        float: Quantification of how unhealthy or indulgent a food item is
    """
    # Calories
    m, b = get_linear_constants((CALORIE_MIN, 0), (CALORIE_MAX, CALORIE_WEIGHT))
    calorie_score = m*total_cals + b
    # Fat %
    m, b = get_linear_constants((PERCENT_FAT_MIN, 0), (PERCENT_FAT_MAX, PERCENT_FAT_WEIGHT))
    fat_score = min(m*total_fat*CALORIES_PER_GRAM_OF_FAT/total_cals + b, PERCENT_FAT_WEIGHT + 1)
    # Sodium
    sodium_score = min(sodium/SODIUM_RDA, SODIUM_WEIGHT + 1)
    # Sugar
    sugar_score = min(sugar/SUGAR_RDA, SUGAR_WEIGHT + 2)

    cheat_score = round(min(calorie_score + fat_score + sodium_score + sugar_score, MAX_CHEAT_SCORE), 2)
    return cheat_score
    
def create_cheat_score_column(meal_items_df):
    # Calculate and add cheat score to the df
    return meal_items_df.apply(lambda df: calculate_cheat_score(df["calories"], df["total_fat"], df["sodium"], df["sugar"]), axis=1)

def remove_restaurants_without_meals(meal_items_df, restaurant_locations_df):
    # Filter out locations which do not have meals in the fastfood dataset
    restaurants = meal_items_df["restaurant"].unique()
    return restaurant_locations_df[restaurant_locations_df["Name"].isin(restaurants)].reset_index(drop=True)

def get_distance(restaurant_name, restaurant_locations_df):
    # Get the distance from the locations df
    df = restaurant_locations_df
    return df.loc[df["Name"]==restaurant_name]["Distance in Km"].values[0]

def get_address(restaurant_name, restaurant_locations_df):
    # Get the address from the locations df
    df = restaurant_locations_df
    return df.loc[df["Name"]==restaurant_name]["Address"].values[0]


def create_distance_and_location_column(meal_items_df, restaurant_locations_df):
    # Create distance and location column from the locations df
    address_col = meal_items_df.apply(lambda df: get_address(df["restaurant"], restaurant_locations_df), axis=1).values.tolist()
    distance_col = meal_items_df.apply(lambda df: get_distance(df["restaurant"], restaurant_locations_df), axis=1).values.tolist()
    return address_col, distance_col

def create_cheat_meals_df(cheat_score_target, meal_items_df):
    """Return a list of potenetial cheat meals based on the cheat score target and distance from the address

    Args:
        cheat_score_target (float): Quantification of food item indulgence level
        meal_items_df (pandas.DataFrame): Contains all available meal items from nearby locations

    Returns:
        pandas.DataFrame: Contains potenial cheat meal options
    """
    # Filter and sort based on target cheat score
    mask1 = meal_items_df["cheat_score"] > (cheat_score_target - CHEAT_SCORE_RANGE)
    mask2 = meal_items_df["cheat_score"] < (cheat_score_target + CHEAT_SCORE_RANGE)
    df = meal_items_df[mask1 & mask2]
    df["score_delta"] = abs(df["cheat_score"] - cheat_score_target)
    return df.sort_values(by=["score_delta", "distance in km"]).reset_index(drop=True)

def get_cheat_meals(address, cheat_score_target, radius, query='fast food', ):
    """Based on address, desired cheat score and max distance from address, return a DataFrame containing potential cheat meal options

    Args:
        address (String): Address from UI.
        query (String, optional): For now, will always be default. Defaults to 'fast food'.
        radius (int): Distance from address allowed.
        cheat_score_target (float): Disired cheat score. 

    Returns:
        pandas.DataFrame: Contains potential cheat meal options
    """
    # Get the search area coordinates
    lat, lng = get_coordinates_from_address(address)
    
    # Create the locations df
    rest_locs_df = create_locations_df(lat, lng, query, radius)

    # Create the menu items df from nearby locations
    menu_items_df = get_restaurant_nutrition_data(rest_locs_df)

    # Add additional informationt to the menu items
    menu_items_df["cheat_score"] = create_cheat_score_column(menu_items_df)
    rest_locs_df = remove_restaurants_without_meals(menu_items_df, rest_locs_df)
    menu_items_df["address"], menu_items_df["distance in km"] = create_distance_and_location_column(menu_items_df, rest_locs_df)

    cheat_meals_df = create_cheat_meals_df(cheat_score_target, menu_items_df)

    return cheat_meals_df


if __name__ == "__main__":
    cheat_meals_df = get_cheat_meals("68 hall avenue guelph on", 7.5, 5000)
    print(cheat_meals_df)