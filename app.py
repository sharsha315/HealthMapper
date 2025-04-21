import streamlit as st
import folium
from streamlit_folium import st_folium
from geo_utils import get_coordinates, fetch_health_facilities

st.set_page_config(page_title="HealthMapper", layout="wide")

st.title("🏥 HealthMapper")
st.write("Find nearby hospitals, clinics, and pharmacies using OpenStreetMap.")

# Input: Location
place = st.text_input("Enter your location:", "Marina Bay, Singapore")

if place:
    lat, lon = get_coordinates(place)
    if lat is None:
        st.error("Could not find the location. Please try again.")
    else:
        st.success(f"Found location: {lat}, {lon}")
        facilities = fetch_health_facilities(lat, lon)

        # Map
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.Marker([lat, lon], tooltip="You are here", icon=folium.Icon(color="blue")).add_to(m)

        for f in facilities:
            icon_color = {"hospital": "red", "clinic": "green", "pharmacy": "purple"}.get(f["type"], "gray")
            folium.Marker(
                location=[f["lat"], f["lon"]],
                tooltip=f"{f['name']} ({f['type']})",
                icon=folium.Icon(color=icon_color)
            ).add_to(m)

        st_folium(m, width=900, height=600)

        st.subheader("📋 Nearby Facilities")
        for f in facilities:
            st.markdown(f"**{f['name']}** - `{f['type'].capitalize()}`")
