import requests
from geopy.geocoders import Nominatim

def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="healthmapper")
    location = geolocator.geocode(place_name)
    if location:
        return location.latitude, location.longitude
    return None, None

def build_overpass_query(lat, lon, radius=5000):
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
      node["amenity"="pharmacy"](around:{radius},{lat},{lon});
    );
    out center;
    """
    return query

def fetch_health_facilities(lat, lon, radius=5000):
    query = build_overpass_query(lat, lon, radius)
    response = requests.post("http://overpass-api.de/api/interpreter", data=query)
    data = response.json()

    facilities = []
    for element in data["elements"]:
        name = element["tags"].get("name", "Unknown")
        facility_type = element["tags"].get("amenity", "Unknown")
        lat = element["lat"]
        lon = element["lon"]
        facilities.append({
            "name": name,
            "type": facility_type,
            "lat": lat,
            "lon": lon
        })
    return facilities
