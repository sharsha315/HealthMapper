import streamlit as st
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# ----------------------------
# Utility Functions
# ----------------------------

@st.cache_data
def get_coordinates(place):
    """Get latitude and longitude from location string using Nominatim."""
    geolocator = Nominatim(user_agent="health-mapper")
    location = geolocator.geocode(place)
    if location:
        return location.latitude, location.longitude
    return None, None

@st.cache_data
def fetch_health_facilities(lat, lon, radius=3000):
    """Fetch health facilities near given coordinates using Overpass API."""
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

# ----------------------------
# Streamlit App
# ----------------------------

st.set_page_config(page_title="HealthMapper", layout="wide")
st.title("🩺 HealthMapper – Nearest Emergency & Health Facilities Finder")

st.markdown("""
Find nearby hospitals, clinics, and pharmacies using **OpenStreetMap** data.  
Simply enter your location and we’ll show you the closest options on a map.
""")

place = st.text_input("Enter a location (e.g. 'Marina Bay, Singapore')")

emergency_mode = st.checkbox("🔴 Emergency Mode (Show only nearest hospitals)", value=False)
facility_options = ["hospital", "clinic", "pharmacy"]

# Input controls
if emergency_mode:
    selected_types = ["hospital"]
    max_results = 3
    radius = 5000
    st.info("Emergency Mode is ON – showing top 3 nearest hospitals.")
else:
    selected_types = st.multiselect("Select facility types to show:", facility_options, default=facility_options)
    max_results = None
    radius = 3000

# Main logic (run only when user has input)
if place:
    lat, lon = get_coordinates(place)
    if lat is None:
        st.error("Could not find the location. Please try again.")
    elif not selected_types:
        st.warning("Please select at least one facility type to proceed.")
    else:
        st.success(f"Found location: {lat:.4f}, {lon:.4f}")
        facilities = fetch_health_facilities(lat, lon, radius=radius)
        st.write(f"Total facilities fetched: {len(facilities)}")

        # Filter selected types
        filtered = [f for f in facilities if f["type"] in selected_types]

        # Add distance and sort
        for f in filtered:
            f["distance_km"] = round(geodesic((lat, lon), (f["lat"], f["lon"])).km, 2)
        filtered.sort(key=lambda x: x["distance_km"])

        if max_results:
            filtered = filtered[:max_results]

        if not filtered:
            st.warning("No facilities found nearby with the selected filters.")
        else:
            # Map setup
            m = folium.Map(location=[lat, lon], zoom_start=14)
            folium.Marker([lat, lon], tooltip="📍 You are here", icon=folium.Icon(color="blue")).add_to(m)

            for f in filtered:
                icon_color = {
                    "hospital": "red",
                    "clinic": "green",
                    "pharmacy": "purple"
                }.get(f["type"], "gray")

                # popup_html = f"""
                # <div style='font-size: 14px;'>
                #     <b>🏥 {f['name']}</b><br>
                #     <b>Type:</b> {f['type'].capitalize()}<br>
                #     <b>Distance:</b> {f['distance_km']} km<br>
                #     <b>🕒 Opening Hours:</b> {f['opening_hours']}<br>
                #     <b>☎️ Contact:</b> {f['contact']}<br>
                #     <b>♿ Wheelchair Access:</b> {f['wheelchair']}<br><br>
                #     <a href="https://www.google.com/maps/dir/?api=1&destination={f['lat']},{f['lon']}" target="_blank" style="color: blue; text-decoration: underline;">
                #         📍 Get Directions via Google Maps
                #     </a>
                # </div>
                #"""
                popup_html = f"""
                <div style='font-size: 14px;'>
                    <b>🏥 {f['name']}</b><br>
                    <b>Type:</b> {f['type'].capitalize()}<br>
                    <b>Distance:</b> {f['distance_km']} km<br>
                """

                if f["opening_hours"] != "Not available":
                    popup_html += f"<b>🕒 Opening Hours:</b> {f['opening_hours']}<br>"

                if f["contact"] != "Not available":
                    popup_html += f"<b>☎️ Contact:</b> {f['contact']}<br>"

                if f["wheelchair"] != "Unknown":
                    popup_html += f"<b>♿ Wheelchair Access:</b> {f['wheelchair']}<br>"

                popup_html += f"""
                    <br>
                    <a href="https://www.google.com/maps/dir/?api=1&destination={f['lat']},{f['lon']}" target="_blank" style="color: blue; text-decoration: underline;">
                        📍 Get Directions via Google Maps
                    </a>
                </div>
                """



                folium.Marker(
                    location=[f["lat"], f["lon"]],
                    tooltip=f"{f['name']} ({f['type']})",
                    icon=folium.Icon(color=icon_color),
                    popup=popup_html
                ).add_to(m)

            st_folium(m, width=900, height=600)

            # List view
            st.subheader("📋 Facility List (sorted by distance)")
            for f in filtered:
                st.markdown(f"**{f['name']}** - `{f['type'].capitalize()}` — {f['distance_km']} km away")
