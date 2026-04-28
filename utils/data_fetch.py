import requests
import random

def get_restaurants():
    url = "https://overpass.kumi.systems/api/interpreter"

    query = """
    [out:json];
    node["amenity"="restaurant"](13.05,80.25,13.12,80.32);
    out;
    """

    try:
        response = requests.get(url, params={'data': query}, timeout=10)

        if response.status_code != 200:
            return []

        data = response.json()

    except Exception as e:
        print("API Error:", e)
        return []

    restaurants = []

    for el in data.get('elements', []):
        if 'tags' in el and 'name' in el['tags']:
            restaurants.append({
                "name": el['tags']['name'],
                "lat": el['lat'],
                "lon": el['lon']
            })

    return restaurants[:15]


# 🔥 THIS FUNCTION WAS MISSING (CAUSE OF ERROR)
def add_food_data(restaurants):
    for r in restaurants:
        r["food"] = random.randint(20, 100)
    return restaurants