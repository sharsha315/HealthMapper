import streamlit as st
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from geo_utils import get_coordinates, fetch_health_facilities

# ----------------------------
# Streamlit App
# ----------------------------

st.set_page_config(page_title="HealthMapper", layout="wide")
st.title("🏥 HealthMapper – Nearest Emergency & Health Facilities Finder")

st.markdown("""
Find nearby hospitals, clinics, and pharmacies using **OpenStreetMap** data.  
Simply enter your location or use your current location to see the closest options.
""")

st.subheader("📍 Detect My Location or Enter a Place")

use_my_location = st.checkbox("Use My Current Location (via browser)")

place = ""
lat = lon = None

if use_my_location:
    loc = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition", key="get_location", debounce=1)
    if loc and loc.get("coords"):
        lat = loc["coords"]["latitude"]
        lon = loc["coords"]["longitude"]
        st.success("✅ Location fetched from browser!")
    else:
        st.warning("⚠️ Could not fetch your location. Please ensure browser permissions are granted.")
else:
    place = st.text_input("Enter a location (e.g. 'Marina Bay, Singapore')")
    if place:
        lat, lon = get_coordinates(place)

emergency_mode = st.checkbox("🔴 Emergency Mode (Show only nearest hospitals)", value=False)
facility_options = ["hospital", "clinic", "pharmacy"]

if emergency_mode:
    selected_types = ["hospital"]
    max_results = 3
    radius = 5000
    st.info("Emergency Mode is ON – showing top 3 nearest hospitals.")
else:
    selected_types = st.multiselect("Select facility types to show:", facility_options, default=facility_options)
    max_results = None
    radius = 3000

if lat and lon:
    if not selected_types:
        st.warning("Please select at least one facility type to proceed.")
    else:
        st.success(f"Found location: {lat:.4f}, {lon:.4f}")
        facilities = fetch_health_facilities(lat, lon, radius=radius)
        st.write(f"Total facilities fetched: {len(facilities)}")

        filtered = [f for f in facilities if f["type"] in selected_types]

        for f in filtered:
            f["distance_km"] = round(geodesic((lat, lon), (f["lat"], f["lon"])) .km, 2)
        filtered.sort(key=lambda x: x["distance_km"])

        if max_results:
            filtered = filtered[:max_results]

        if not filtered:
            st.warning("No facilities found nearby with the selected filters.")
        else:
            m = folium.Map(location=[lat, lon], zoom_start=14)
            folium.Marker([lat, lon], tooltip="📍 You are here", icon=folium.Icon(color="blue")).add_to(m)

            icon_map = {"hospital": "red", "clinic": "green", "pharmacy": "purple"}

            for f in filtered:
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
                    icon=folium.Icon(color=icon_map.get(f["type"], "gray")),
                    popup=popup_html
                ).add_to(m)

            st_folium(m, width=900, height=600)

            type_counts = {t: sum(1 for f in filtered if f["type"] == t) for t in selected_types}
            summary = " | ".join([f"{t.capitalize()}: {count}" for t, count in type_counts.items()])
            st.markdown(f"### 💡 Facility Count Summary: {summary}")

            if filtered:
                avg_distance = sum(f["distance_km"] for f in filtered) / len(filtered)
                st.info(f"📊 Average Distance to Facilities: **{avg_distance:.2f} km**")

            icon_emojis = {"hospital": "🏥", "clinic": "🩺", "pharmacy": "💊"}
            st.subheader("📋 Facility List (Grouped by Type)")
            for ftype in ["hospital", "clinic", "pharmacy"]:
                group = [f for f in filtered if f["type"] == ftype]
                if not group:
                    continue
                st.markdown(f"#### {icon_emojis.get(ftype, '📍')} {ftype.capitalize()}s")
                for f in group:
                    gmaps_url = f"https://www.google.com/maps/search/?api=1&query={f['lat']},{f['lon']}"
                    st.markdown(f"- [{f['name']}]({gmaps_url}) — {f['distance_km']} km away")
else:
    st.info("Please enter a location or allow access to your current location to begin.")

