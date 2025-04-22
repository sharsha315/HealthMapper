# 🏥 HealthMapper

## ✅ Project Overview:

**HealthMapper** is a lightweight, location-aware web application that helps users instantly locate the nearest **hospitals**, **clinics**, and **pharmacies** using **OpenStreetMap** and the **Overpass API**. Built with Python and Streamlit, this tool is ideal for emergencies and general health planning.

---

## 🌟 Features

- 🔍 **Smart Search**: Enter a place manually or use your **current GPS location** (with browser permission)
- 🏥 **Emergency Mode**: Filters and shows **only nearest hospitals** (top 3)
- 🗺️ **Interactive Map**: Facility markers with distance, type, opening hours, contact & wheelchair access info
- 📋 **Categorized List View**: Facilities grouped by type for quick skimming
- 📏 **Distance Calculations**: Each facility’s distance from your location shown in km
- 📊 **Summary Statistics**: Total counts and average distance to all shown facilities

---

> 👉 Useful for emergency responders, travelers, public health initiatives, or anyone needing quick access to care.

## 🚀 Getting Started

### 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/sharsha315/HealthMapper.git
cd HealthMapper
```

2. Create Virutal Environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

---


## 🎥 Demo Video

> Link to Demo Video here


## 📦 Folder Structure

```
healthmapper/
├── app.py                # Main Streamlit app
├── geo_utils.py         # Location and Overpass API utilities
├── requirements.txt     # Python dependencies
├── README.md            # Project overview and documentation
└── ...
```

---

## 📍 Data Source

- [OpenStreetMap](https://www.openstreetmap.org/)
- [Overpass API](https://overpass-api.de/)

All health facility data is fetched in real-time from OSM via Overpass.

---

## 💡 Use Cases

- Tourists needing quick access to pharmacies or clinics
- Emergency responders and caregivers
- Anyone in a new city looking for nearby healthcare

---

## 🙌 Acknowledgements

- Icons & Emojis via Streamlit and Unicode
- Mapping powered by Folium and Leaflet

---

## 📃 License

This project is open source under the [MIT License](https://github.com/sharsha315/HealthMapper/blob/main/LICENSE).

---

## 🧑‍💻 Author
Made with ❤️ by Harsha S
- Discord: **sharsha315**
- X (Twitter): [**@sharsha315**](https://www.x.com/sharsha315)