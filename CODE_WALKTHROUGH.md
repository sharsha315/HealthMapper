# 🧠 CODE_WALKTHROUGH.md

This document explains the core code structure and functionality of the **HealthMapper** project. It is intended to give developers and reviewers a quick overview of how the application works under the hood.

---

## 📁 Project Structure

```bash
.
├── app.py                 # Main Streamlit frontend code
├── geo_utils.py          # Utility functions: geocoding, Overpass API queries
├── requirements.txt       # Python dependencies
├── README.md              # Project summary and instructions
├── CODE_WALKTHROUGH.md    # This file
```

---

## 🔧 `geo_utils.py`
This module handles location-based utilities and API requests.

### ✅ `get_coordinates(place)`
Uses **Geopy** and **Nominatim** to geocode a place name to latitude and longitude.
```python
geolocator = Nominatim(user_agent="health-mapper")
location = geolocator.geocode(place)
```

### ✅ `fetch_health_facilities(lat, lon, radius)`
Constructs an Overpass QL query to fetch hospitals, clinics, and pharmacies near a point.
```python
query = f"""
  node["amenity"="hospital"](around:{radius},{lat},{lon});
  node["amenity"="clinic"](around:{radius},{lat},{lon});
  node["amenity"="pharmacy"](around:{radius},{lat},{lon});
"""
```
---

## 🖥️ `app.py`
This is the main file that runs the Streamlit application.

### ✅ Location Input Options
* Uses a **checkbox** to toggle between browser-based geolocation and manual place input.
* Uses `streamlit_js_eval` to fetch current coordinates if permission is granted.

### ✅ Facility Selection
* Dropdown to select types of facilities: hospital, clinic, pharmacy.
* **Emergency mode** available to show only top 3 nearest hospitals.

### ✅ Facility Filtering and Sorting
* Computes geodesic distance using **Geopy**.
* Filters based on selected types.
* Sorts facilities by distance.

### ✅ Interactive Map
* Built using **Folium**, shows all filtered results with custom icons and popups.
* User’s location is marked separately.

### ✅ Grouped Facility Display
* Results are grouped by categories and displayed with emojis.
* Each facility is listed with clickable Google Maps link.

---

## 📦 Dependencies
Installed from `requirements.txt`, includes:
* streamlit
* geopy
* folium
* requests
* streamlit_folium
* streamlit_js_eval

---

## ✅ Summary
HealthMapper is modular, readable, and easy to extend. Utility functions are separated in `geo_utils.py`, and Streamlit code in `app.py` is user-friendly and interactive.

This walkthrough gives you a solid head start if you want to contribute or understand the logic behind the application.

---

