# ---- pages/2_Recommendations.py ----
import streamlit as st
import joblib
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db_functions
import header

st.set_page_config(page_title="Crop Recommendations", page_icon="✅", layout="wide", initial_sidebar_state="collapsed")
def load_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), '..', file_name)
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style.css")
header.custom_header("Recommendations")

def get_weather(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return {"temperature": data["main"]["temp"], "humidity": data["main"]["humidity"]}
        else:
            return {"temperature": 25.0, "humidity": 70.0}
    except Exception:
        return {"temperature": 25.0, "humidity": 70.0}

try:
    crop_model = joblib.load("crop_model.joblib")
except Exception:
    st.error("crop_model.joblib not found.")
    crop_model = None

st.title("Crop Recommendation Tool")

# --- Location Selection Card ---
with st.container(border=True):
    st.subheader("📍 Location Selection")
    search_query = st.text_input("Search for a location")
    if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lon = 12.9716, 77.5946
    if search_query:
        try:
            geolocator = Nominatim(user_agent="crop_recommender")
            location = geolocator.geocode(search_query)
            if location: st.session_state.lat, st.session_state.lon = location.latitude, location.longitude
        except Exception: st.warning("Geocoding failed.")
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=10)
    folium.Marker([st.session_state.lat, st.session_state.lon]).add_to(m)
    map_data = st_folium(m, height=350, use_container_width=True)
    if map_data and map_data.get("last_clicked"):
        clicked_lat, clicked_lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        if (st.session_state.lat != clicked_lat) or (st.session_state.lon != clicked_lon):
            st.session_state.lat, st.session_state.lon = clicked_lat, clicked_lon
            st.rerun()

# --- Input Parameters Card ---
weather_data = get_weather(st.session_state.lat, st.session_state.lon)
with st.container(border=True):
    st.subheader("🧪 Input Parameters")
    form_col1, form_col2 = st.columns(2)
    with form_col1:
        n, p, k = st.slider("Nitrogen (N)", 0, 140, 50), st.slider("Phosphorus (P)", 5, 145, 50), st.slider("Potassium (K)", 5, 205, 50)
    with form_col2:
        temp = st.slider("Temperature (°C)", 8.0, 50.0, value=float(weather_data["temperature"]), step=0.1)
        humidity = st.slider("Humidity (%)", 14.0, 100.0, value=float(weather_data["humidity"]), step=0.1)
        ph = st.slider("Soil pH", 3.5, 9.9, 6.5, 0.1)
    rainfall = st.slider("Rainfall (mm)", 20.0, 300.0, 100.0, 0.1)
    submitted = st.button("Get Recommendations")

# --- Recommended Crops Card ---
with st.container(border=True):
    st.subheader("✅ Recommended Crops")
    if "recommendations" not in st.session_state: st.session_state.recommendations = []
    if submitted:
        if crop_model:
            with st.spinner("Analyzing..."):
                data = {"nitrogen": n, "phosphorus": p, "potassium": k, "temperature": temp, "humidity": humidity, "ph": ph, "rainfall": rainfall}
                features = [list(data.values())]
                probabilities = crop_model.predict_proba(features)[0]
                crop_probabilities = list(zip(crop_model.classes_, probabilities))
                top_crops = sorted(crop_probabilities, key=lambda item: item[1], reverse=True)[:3]
                st.session_state.recommendations = top_crops
                if top_crops: db_functions.save_recommendation(data, top_crops[0][0].capitalize())
        else: st.error("Model not loaded.")
    if st.session_state.recommendations:
        for crop, confidence in st.session_state.recommendations:
            st.markdown(f'<div class="recommendation-item"><p style="font-weight: bold; color: #1E8449;">{crop.capitalize()}</p><p style.fontSize = "0.9em"; color: #566573;>Confidence: {confidence*100:.1f}%</p></div>', unsafe_allow_html=True)
    else:
        st.info("Results will appear here after you click 'Get Recommendations'.")

