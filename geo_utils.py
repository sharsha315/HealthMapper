import streamlit as st
import requests
from geopy.geocoders import Nominatim

@st.cache_data
def get_coordinates(place):
    geolocator = Nominatim(user_agent="health-mapper")
    location = geolocator.geocode(place)
    if location:
        return location.latitude, location.longitude
    return None, None

@st.cache_data
def fetch_health_facilities(lat, lon, radius=3000):
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
      node["amenity"="pharmacy"](around:{radius},{lat},{lon});
    );
    out body;
    """
    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": query})
    facilities = []
    if response.status_code == 200:
        data = response.json()
        for element in data["elements"]:
            tags = element.get("tags", {})
            facility = {
                "name": tags.get("name", "Unnamed"),
                "type": tags.get("amenity", "unknown"),
                "lat": element["lat"],
                "lon": element["lon"],
                "opening_hours": tags.get("opening_hours", "Not available"),
                "contact": tags.get("contact:phone") or tags.get("phone") or "Not available",
                "wheelchair": tags.get("wheelchair", "Unknown"),
            }
            facilities.append(facility)
    return facilities