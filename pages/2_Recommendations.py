# # ---- pages/2_Recommendations.py ----
# import streamlit as st
# import joblib
# from streamlit_folium import st_folium
# import folium
# from geopy.geocoders import Nominatim
# import requests
# import sys
# import os

# # --- Correctly set up the path to import shared files ---
# # This script is in the 'pages' folder, so we go up one level to the root
# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(ROOT_DIR)

# import db_functions
# import crop_data

# st.set_page_config(page_title="Crop Recommendations", page_icon="✅", layout="wide", initial_sidebar_state="expanded")

# def load_css(file_name):
#     # Construct the correct, absolute path to the CSS file from the root
#     css_path = os.path.join(ROOT_DIR, file_name)
#     with open(css_path) as f: 
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# load_css("style.css")

# # --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# # --- ADD THIS SECTION FOR SIDEBAR NAVIGATION ---
# # Import and call the function that creates your sidebar navigation
# # Make sure you have a function like this in one of your shared modules
# # Create basic sidebar navigation
# st.sidebar.title("🌱 AgriAssist")
# st.sidebar.page_link("app.py", label="Home")
# st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard")
# st.sidebar.page_link("pages/2_Recommendations.py", label="Recommendations")
# st.sidebar.page_link("pages/3_Insights.py", label="Insights")
# st.sidebar.page_link("pages/4_History.py", label="History")
# st.sidebar.page_link("pages/5_Support.py", label="Support")
# st.sidebar.page_link("pages/6_Profile.py", label="Profile")

# # Add admin page for admin users
# if st.session_state.get('role') == 'Admin':
#     st.sidebar.page_link("pages/7_Admin_Dashboard.py", label="Admin Dashboard")

# # Logout button
# if st.sidebar.button("Logout"):
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]
#     st.rerun()

# TIPS = [
#     "**Soil Testing:** Regularly test your soil to understand its nutrient profile and pH level for accurate recommendations.",
#     "**Crop Rotation:** Avoid planting the same crop in the same place year after year to manage pests and improve soil health.",
#     "**Water Management:** Use efficient irrigation methods like drip irrigation to conserve water.",
#     "**Integrated Pest Management (IPM):** Combine biological, cultural, and chemical practices to manage pests sustainably."
# ]

# def get_weather(lat, lon):
#     try:
#         api_key = st.secrets["OPENWEATHER_API_KEY"]
#         url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
#         response = requests.get(url, timeout=5).json()
#         return {"temperature": response["main"]["temp"], "humidity": response["main"]["humidity"]}
#     except Exception:
#         st.warning("Could not fetch live weather data. Using default values.")
#         return {"temperature": 25.0, "humidity": 70.0}

# try:
#     # Construct the correct, absolute path to the model file from the root
#     model_path = os.path.join(ROOT_DIR, 'crop_model.joblib')
#     crop_model = joblib.load(model_path)
# except Exception:
#     st.error("crop_model.joblib not found in the main project folder.")
#     crop_model = None

# st.title("🌾 Crop Recommendation Tool")
# st.markdown(
#     "<p style='font-size: 1.1rem; color: #059669; margin-bottom: 2rem; font-weight: 500;'>"
#     "Get AI-powered crop recommendations based on soil conditions, weather, and location data.</p>",
#     unsafe_allow_html=True
# )

# with st.expander("🔎 Explore Crops by Season or Type"):
#     col1, col2 = st.columns(2)
#     with col1:
#         season = st.selectbox("Filter by Season", options=list(crop_data.CROP_FILTER_DATA['seasons'].keys()))
#         st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['seasons'][season])}</div>", unsafe_allow_html=True)
#     with col2:
#         crop_type = st.selectbox("Filter by Type", options=list(crop_data.CROP_FILTER_DATA['types'].keys()))
#         st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['types'][crop_type])}</div>", unsafe_allow_html=True)

# # --- Location Selection Card ---
# with st.container(border=True):
#     st.subheader("📍 Location Selection")
#     search_query = st.text_input("Search for a location")
#     if 'lat' not in st.session_state: st.session_state.lat, st.session_state.lon = 12.9716, 77.5946
#     if search_query:
#         try:
#             geolocator = Nominatim(user_agent="crop_recommender")
#             location = geolocator.geocode(search_query)
#             if location: st.session_state.lat, st.session_state.lon = location.latitude, location.longitude
#         except Exception: st.warning("Geocoding failed.")
#     m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=10)
#     folium.Marker([st.session_state.lat, st.session_state.lon]).add_to(m)
#     map_data = st_folium(m, height=350, use_container_width=True)
#     if map_data and map_data.get("last_clicked"):
#         clicked_lat, clicked_lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
#         if (st.session_state.lat, st.session_state.lon) != (clicked_lat, clicked_lon):
#             st.session_state.lat, st.session_state.lon = clicked_lat, clicked_lon
#             st.rerun()

# # --- Input Parameters Card ---
# weather_data = get_weather(st.session_state.lat, st.session_state.lon)
# with st.container(border=True):
#     st.subheader("🧪 Input Parameters")
#     form_col1, form_col2 = st.columns(2)
#     with form_col1:
#         n, p, k = st.slider("Nitrogen (N)", 0, 140, 50), st.slider("Phosphorus (P)", 5, 145, 50), st.slider("Potassium (K)", 5, 205, 50)
#     with form_col2:
#         temp_val = max(8.0, min(50.0, float(weather_data["temperature"])))
#         hum_val = max(14.0, min(100.0, float(weather_data["humidity"])))
#         temp = st.slider("Temperature (°C)", 8.0, 50.0, temp_val, 0.1)
#         humidity = st.slider("Humidity (%)", 14.0, 100.0, hum_val, 0.1)
#         ph = st.slider("Soil pH", 3.5, 9.9, 6.5, 0.1)
#     rainfall = st.slider("Rainfall (mm)", 20.0, 300.0, 100.0, 0.1)
#     submitted = st.button("Get Recommendations")

# # --- Tips Section ---
# with st.container(border=True):
#     st.subheader("💡 Agricultural Tips")
#     for tip in TIPS: st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)

# # --- Recommended Crops Card (at the bottom) ---
# with st.container(border=True):
#     st.subheader("✅ Recommended Crops")
#     if "recommendations" not in st.session_state: st.session_state.recommendations = []
#     if submitted and crop_model:
#         with st.spinner("Analyzing..."):
#             data = {"nitrogen": n, "phosphorus": p, "potassium": k, "temperature": temp, "humidity": humidity, "ph": ph, "rainfall": rainfall}
#             features = [list(data.values())]
#             probabilities = crop_model.predict_proba(features)[0]
#             crop_probabilities = list(zip(crop_model.classes_, probabilities))
#             top_crops = sorted(crop_probabilities, key=lambda i: i[1], reverse=True)[:3]
#             st.session_state.recommendations = []
#             for crop, confidence in top_crops:
#                 rec_id = db_functions.save_recommendation(data, crop.capitalize())
#                 st.session_state.recommendations.append({'id': rec_id, 'crop': crop, 'confidence': confidence, 'status': 'new'})
    
#     if st.session_state.recommendations:
#         rec_cols = st.columns(3)
#         for i, rec in enumerate(st.session_state.recommendations):
#             with rec_cols[i]:
#                 is_done = (rec['status'] == 'done')
#                 done_class = "done" if is_done else ""
#                 st.markdown(f'<div class="recommendation-item {done_class}">', unsafe_allow_html=True)
                
#                 relative_image_path = crop_data.CROP_IMAGES.get(rec['crop'].lower(), crop_data.CROP_IMAGES['default'])
#                 full_image_path = os.path.join(ROOT_DIR, relative_image_path)
                
#                 if os.path.exists(full_image_path):
#                     st.image(full_image_path)
#                 else:
#                     st.warning(f"Image not found")

#                 details = crop_data.CROP_DETAILS.get(rec['crop'].lower(), crop_data.CROP_DETAILS['default'])
#                 st.markdown(f"**{rec['crop'].capitalize()}**")
#                 st.markdown(f"<small>Confidence: {rec['confidence']*100:.1f}%</small>", unsafe_allow_html=True)
#                 st.markdown(f"<small>{details['description']}</small>", unsafe_allow_html=True)
#                 st.markdown(f"<small>💧 Water: {details['water']} | ⚖️ Yield: {details['yield']}</small>", unsafe_allow_html=True)
#                 if not is_done:
#                     if st.button("Mark as Done", key=f"done_{rec['id']}"):
#                         db_functions.mark_as_done(rec['id'])
#                         st.session_state.recommendations[i]['status'] = 'done'
#                         st.rerun()
#                 else:
#                     st.success("✔️ Done")
#                 st.markdown('</div>', unsafe_allow_html=True)
#     else:
#         st.info("Results will appear here.")

# ---- pages/2_Recommendations.py ----
# import streamlit as st
# import joblib
# from streamlit_folium import st_folium
# import folium
# from geopy.geocoders import Nominatim
# import requests
# import sys
# import os
# import warnings
# import traceback

# # Suppress warnings
# warnings.filterwarnings('ignore')

# # --- Correctly set up the path to import shared files ---
# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(ROOT_DIR)

# import db_functions
# import crop_data

# st.set_page_config(
#     page_title="Crop Recommendations", 
#     page_icon="✅", 
#     layout="wide", 
#     initial_sidebar_state="expanded"
# )

# def load_css(file_name):
#     css_path = os.path.join(ROOT_DIR, file_name)
#     try:
#         with open(css_path) as f: 
#             st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#     except FileNotFoundError:
#         st.warning(f"CSS file not found: {css_path}")

# load_css("style.css")

# # --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# # --- Sidebar Navigation ---
# st.sidebar.title("🌱 AgriAssist")
# st.sidebar.page_link("app.py", label="Home")
# st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard")
# st.sidebar.page_link("pages/2_Recommendations.py", label="Recommendations", disabled=True)
# st.sidebar.page_link("pages/3_Insights.py", label="Insights")
# st.sidebar.page_link("pages/4_History.py", label="History")
# st.sidebar.page_link("pages/5_Support.py", label="Support")
# st.sidebar.page_link("pages/6_Profile.py", label="Profile")

# if st.session_state.get('role') == 'Admin':
#     st.sidebar.page_link("pages/7_Admin_Dashboard.py", label="Admin Dashboard")

# st.sidebar.markdown("---")
# st.sidebar.markdown(f"**User:** {st.session_state.get('username', 'Unknown')}")

# if st.sidebar.button("Logout", type="primary"):
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]
#     st.rerun()

# TIPS = [
#     "**Soil Testing:** Regularly test your soil to understand its nutrient profile and pH level for accurate recommendations.",
#     "**Crop Rotation:** Avoid planting the same crop in the same place year after year to manage pests and improve soil health.",
#     "**Water Management:** Use efficient irrigation methods like drip irrigation to conserve water.",
#     "**Integrated Pest Management (IPM):** Combine biological, cultural, and chemical practices to manage pests sustainably."
# ]

# def get_weather(lat, lon):
#     try:
#         api_key = st.secrets.get("OPENWEATHER_API_KEY", "")
#         if not api_key:
#             return {"temperature": 25.0, "humidity": 70.0}
            
#         url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
#         response = requests.get(url, timeout=10).json()
#         return {"temperature": response["main"]["temp"], "humidity": response["main"]["humidity"]}
#     except Exception:
#         return {"temperature": 25.0, "humidity": 70.0}

# def create_map(lat, lon):
#     try:
#         m = folium.Map(location=[lat, lon], zoom_start=10)
#         folium.Marker([lat, lon]).add_to(m)
#         return m
#     except Exception:
#         return None

# # Load model safely
# try:
#     model_path = os.path.join(ROOT_DIR, 'crop_model.joblib')
#     crop_model = joblib.load(model_path)
# except Exception as e:
#     st.error(f"Model loading error: {e}")
#     crop_model = None

# st.title("Crop Recommendation Tool")

# try:
#     # Main content
#     with st.expander("🔎 Explore Crops by Season or Type"):
#         col1, col2 = st.columns(2)
#         with col1:
#             season = st.selectbox("Filter by Season", options=list(crop_data.CROP_FILTER_DATA['seasons'].keys()))
#             st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['seasons'][season])}</div>", unsafe_allow_html=True)
#         with col2:
#             crop_type = st.selectbox("Filter by Type", options=list(crop_data.CROP_FILTER_DATA['types'].keys()))
#             st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['types'][crop_type])}</div>", unsafe_allow_html=True)

#     # Initialize session state for location
#     if 'lat' not in st.session_state:
#         st.session_state.lat, st.session_state.lon = 12.9716, 77.5946

#     # Location Selection
#     with st.container(border=True):
#         st.subheader("📍 Location Selection")
#         search_query = st.text_input("Search for a location")
        
#         if search_query:
#             try:
#                 geolocator = Nominatim(user_agent="crop_recommender_app")
#                 location = geolocator.geocode(search_query, timeout=10)
#                 if location:
#                     st.session_state.lat, st.session_state.lon = location.latitude, location.longitude
#                     st.success(f"Location found: {location.address}")
#             except Exception:
#                 st.warning("Geocoding service unavailable. Using default location.")
        
#         m = create_map(st.session_state.lat, st.session_state.lon)
#         if m:
#             map_data = st_folium(m, height=350, use_container_width=True, key="main_map")
#             if map_data and map_data.get("last_clicked"):
#                 clicked_lat = map_data["last_clicked"]["lat"]
#                 clicked_lon = map_data["last_clicked"]["lng"]
#                 st.session_state.lat, st.session_state.lon = clicked_lat, clicked_lon
#                 st.rerun()
#         else:
#             st.error("Failed to load map")

#     # Input Parameters
#     weather_data = get_weather(st.session_state.lat, st.session_state.lon)
#     with st.container(border=True):
#         st.subheader("🧪 Input Parameters")
#         form_col1, form_col2 = st.columns(2)
#         with form_col1:
#             n = st.slider("Nitrogen (N)", 0, 140, 50, step=1)
#             p = st.slider("Phosphorus (P)", 5, 145, 50, step=1)
#             k = st.slider("Potassium (K)", 5, 205, 50, step=1)
#         with form_col2:
#             temp_val = max(8.0, min(50.0, float(weather_data["temperature"])))
#             hum_val = max(14.0, min(100.0, float(weather_data["humidity"])))
#             temp = st.slider("Temperature (°C)", 8.0, 50.0, temp_val, 0.1, step=0.1)
#             humidity = st.slider("Humidity (%)", 14.0, 100.0, hum_val, 0.1, step=0.1)
#             ph = st.slider("Soil pH", 3.5, 9.9, 6.5, 0.1, step=0.1)
#         rainfall = st.slider("Rainfall (mm)", 20.0, 300.0, 100.0, 0.1, step=0.1)
#         submitted = st.button("Get Recommendations", type="primary")

#     # Tips Section
#     with st.container(border=True):
#         st.subheader("💡 Agricultural Tips")
#         for tip in TIPS: 
#             st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)

#     # Recommendations
#     with st.container(border=True):
#         st.subheader("✅ Recommended Crops")
        
#         if "recommendations" not in st.session_state:
#             st.session_state.recommendations = []
            
#         if submitted and crop_model:
#             with st.spinner("Analyzing soil and weather conditions..."):
#                 try:
#                     data = {
#                         "nitrogen": n, "phosphorus": p, "potassium": k, 
#                         "temperature": temp, "humidity": humidity, 
#                         "ph": ph, "rainfall": rainfall
#                     }
#                     features = [list(data.values())]
#                     probabilities = crop_model.predict_proba(features)[0]
#                     crop_probabilities = list(zip(crop_model.classes_, probabilities))
#                     top_crops = sorted(crop_probabilities, key=lambda i: i[1], reverse=True)[:3]
                    
#                     st.session_state.recommendations = []
#                     for crop, confidence in top_crops:
#                         rec_id = db_functions.save_recommendation(data, crop.capitalize())
#                         st.session_state.recommendations.append({
#                             'id': rec_id, 
#                             'crop': crop, 
#                             'confidence': confidence, 
#                             'status': 'new'
#                         })
                        
#                 except Exception as e:
#                     st.error(f"Analysis failed: {str(e)}")
        
#         # Display recommendations
#         if st.session_state.recommendations:
#             rec_cols = st.columns(3)
#             for i, rec in enumerate(st.session_state.recommendations):
#                 with rec_cols[i]:
#                     is_done = (rec['status'] == 'done')
#                     done_class = "done" if is_done else ""
#                     st.markdown(f'<div class="recommendation-item {done_class}">', unsafe_allow_html=True)
                    
#                     relative_image_path = crop_data.CROP_IMAGES.get(rec['crop'].lower(), crop_data.CROP_IMAGES['default'])
#                     full_image_path = os.path.join(ROOT_DIR, relative_image_path)
                    
#                     if os.path.exists(full_image_path):
#                         st.image(full_image_path, use_container_width=True)
#                     else:
#                         st.info("🌱 Default crop image")
                    
#                     details = crop_data.CROP_DETAILS.get(rec['crop'].lower(), crop_data.CROP_DETAILS['default'])
#                     st.markdown(f"**{rec['crop'].capitalize()}**")
#                     st.markdown(f"*Confidence: {rec['confidence']*100:.1f}%*")
#                     st.markdown(f"{details['description']}")
#                     st.markdown(f"💧 Water: {details['water']} | ⚖️ Yield: {details['yield']}")
                    
#                     if not is_done:
#                         if st.button("Mark as Done", key=f"done_{rec['id']}"):
#                             db_functions.mark_as_done(rec['id'])
#                             st.session_state.recommendations[i]['status'] = 'done'
#                             st.rerun()
#                     else:
#                         st.success("✔️ Done")
#                     st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             st.info("👆 Click 'Get Recommendations' to see suggested crops for your conditions")

# except Exception as e:
#     st.error("An error occurred on this page")
#     if st.checkbox("Show error details"):
#         st.code(traceback.format_exc())

# ---- pages/2_Recommendations.py ----
# import streamlit as st
# import joblib
# from streamlit_folium import st_folium
# import folium
# from geopy.geocoders import Nominatim
# import requests
# import sys
# import os
# import warnings
# import traceback

# # Suppress warnings
# warnings.filterwarnings('ignore')

# # --- Correctly set up the path to import shared files ---
# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(ROOT_DIR)

# import db_functions
# import crop_data

# st.set_page_config(
#     page_title="Crop Recommendations",
#     page_icon="✅",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# def load_css(file_name):
#     css_path = os.path.join(ROOT_DIR, file_name)
#     try:
#         with open(css_path) as f:
#             st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#     except FileNotFoundError:
#         st.warning(f"CSS file not found: {css_path}")

# load_css("style.css")

# # --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# # --- Sidebar Navigation ---
# st.sidebar.title("🌱 AgriAssist")
# st.sidebar.page_link("app.py", label="Home")
# st.sidebar.page_link("pages/1_Dashboard.py", label="Dashboard")
# st.sidebar.page_link("pages/2_Recommendations.py", label="Recommendations", disabled=True)
# st.sidebar.page_link("pages/3_Insights.py", label="Insights")
# st.sidebar.page_link("pages/4_History.py", label="History")
# st.sidebar.page_link("pages/5_Support.py", label="Support")
# st.sidebar.page_link("pages/6_Profile.py", label="Profile")

# if st.session_state.get('role') == 'Admin':
#     st.sidebar.page_link("pages/7_Admin_Dashboard.py", label="Admin Dashboard")

# st.sidebar.markdown("---")
# st.sidebar.markdown(f"**User:** {st.session_state.get('username', 'Unknown')}")

# if st.sidebar.button("Logout", type="primary"):
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]
#     st.rerun()

# TIPS = [
#     "**Soil Testing:** Regularly test your soil to understand its nutrient profile and pH level for accurate recommendations.",
#     "**Crop Rotation:** Avoid planting the same crop in the same place year after year to manage pests and improve soil health.",
#     "**Water Management:** Use efficient irrigation methods like drip irrigation to conserve water.",
#     "**Integrated Pest Management (IPM):** Combine biological, cultural, and chemical practices to manage pests sustainably."
# ]

# # --- Helper functions ---
# def get_weather(lat, lon):
#     try:
#         api_key = st.secrets.get("OPENWEATHER_API_KEY", "")
#         if not api_key:
#             return {"temperature": 25.0, "humidity": 70.0}

#         url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
#         response = requests.get(url, timeout=10).json()
#         return {"temperature": response["main"]["temp"], "humidity": response["main"]["humidity"]}
#     except Exception:
#         return {"temperature": 25.0, "humidity": 70.0}

# def create_map(lat, lon, address=None):
#     """Create map centered on given coordinates with marker and tooltip"""
#     try:
#         m = folium.Map(location=[lat, lon], zoom_start=10)
#         popup_text = address if address else f"Lat: {lat:.4f}, Lon: {lon:.4f}"
#         folium.Marker(
#             [lat, lon],
#             popup=popup_text,
#             tooltip="📍 Click to move marker",
#             icon=folium.Icon(color="green", icon="leaf")
#         ).add_to(m)
#         return m
#     except Exception:
#         return None

# def reverse_geocode(lat, lon):
#     """Convert coordinates to address"""
#     try:
#         geolocator = Nominatim(user_agent="crop_recommender_app")
#         location = geolocator.reverse((lat, lon), timeout=10)
#         return location.address if location else "Address not found"
#     except Exception:
#         return "Address lookup failed"

# def geocode_address(search_query):
#     """Convert address to coordinates"""
#     try:
#         geolocator = Nominatim(user_agent="crop_recommender_app")
#         location = geolocator.geocode(search_query, timeout=10)
#         if location:
#             return location.latitude, location.longitude, location.address
#         return None, None, None
#     except Exception:
#         return None, None, None

# # Load model safely
# try:
#     model_path = os.path.join(ROOT_DIR, 'crop_model.joblib')
#     crop_model = joblib.load(model_path)
# except Exception as e:
#     st.error(f"Model loading error: {e}")
#     crop_model = None

# # --- Default location: Bangalore ---
# DEFAULT_LAT, DEFAULT_LON = 12.9716, 77.5946
# DEFAULT_ADDRESS = "Bangalore, Karnataka, India"

# # Initialize session state for location and address
# if "lat" not in st.session_state:
#     st.session_state.lat = DEFAULT_LAT
# if "lon" not in st.session_state:
#     st.session_state.lon = DEFAULT_LON
# if "address" not in st.session_state:
#     st.session_state.address = DEFAULT_ADDRESS

# # --- PAGE CONTENT ---
# st.title("Crop Recommendation Tool")

# try:
#     # --- Crop Filter Section ---
#     with st.expander("🔎 Explore Crops by Season or Type"):
#         col1, col2 = st.columns(2)
#         with col1:
#             season = st.selectbox("Filter by Season", options=list(crop_data.CROP_FILTER_DATA['seasons'].keys()))
#             st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['seasons'][season])}</div>", unsafe_allow_html=True)
#         with col2:
#             crop_type = st.selectbox("Filter by Type", options=list(crop_data.CROP_FILTER_DATA['types'].keys()))
#             st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['types'][crop_type])}</div>", unsafe_allow_html=True)

#     # --- Location Section ---
#     with st.container(border=True):
#         st.subheader("📍 Location Selection")

#         # Display current info
#         st.markdown(f"**Current Coordinates:** 🌐 {st.session_state.lat:.4f}, {st.session_state.lon:.4f}")
#         st.markdown(f"**Address:** 🏡 {st.session_state.address}")

#         # Search bar with clear button
#         search_col, clear_col = st.columns([4, 1])
#         with search_col:
#             search_query = st.text_input("Search for a location", value=st.session_state.address)
#         with clear_col:
#             if st.button("🧭 Clear", help="Reset to default Bangalore location"):
#                 st.session_state.lat = DEFAULT_LAT
#                 st.session_state.lon = DEFAULT_LON
#                 st.session_state.address = DEFAULT_ADDRESS
#                 st.rerun()

#         # Handle search input
#         if search_query and search_query != st.session_state.address:
#             lat, lon, address = geocode_address(search_query)
#             if lat and lon:
#                 st.session_state.lat, st.session_state.lon, st.session_state.address = lat, lon, address
#                 st.success(f"✅ Found location: {address}")
#             else:
#                 st.warning("⚠️ Could not find location, keeping previous.")

#         # Create and show map
#         m = create_map(st.session_state.lat, st.session_state.lon, st.session_state.address)
#         if m:
#             map_data = st_folium(m, height=350, use_container_width=True, key="main_map")
#             if map_data and map_data.get("last_clicked"):
#                 clicked_lat = map_data["last_clicked"]["lat"]
#                 clicked_lon = map_data["last_clicked"]["lng"]
#                 st.session_state.lat, st.session_state.lon = clicked_lat, clicked_lon
#                 st.session_state.address = reverse_geocode(clicked_lat, clicked_lon)
#                 st.rerun()
#         else:
#             st.error("❌ Failed to load map")

#     # --- Input Parameters ---
#     weather_data = get_weather(st.session_state.lat, st.session_state.lon)
#     with st.container(border=True):
#         st.subheader("🧪 Input Parameters")
#         form_col1, form_col2 = st.columns(2)
#         with form_col1:
#             n = st.slider("Nitrogen (N)", 0, 140, 50, step=1)
#             p = st.slider("Phosphorus (P)", 5, 145, 50, step=1)
#             k = st.slider("Potassium (K)", 5, 205, 50, step=1)
#         with form_col2:
#             temp_val = max(8.0, min(50.0, float(weather_data["temperature"])))
#             hum_val = max(14.0, min(100.0, float(weather_data["humidity"])))
#             temp = st.slider("Temperature (°C)", 8.0, 50.0, temp_val, 0.1, step=0.1)
#             humidity = st.slider("Humidity (%)", 14.0, 100.0, hum_val, 0.1, step=0.1)
#             ph = st.slider("Soil pH", 3.5, 9.9, 6.5, 0.1, step=0.1)
#         rainfall = st.slider("Rainfall (mm)", 20.0, 300.0, 100.0, 0.1, step=0.1)
#         submitted = st.button("Get Recommendations", type="primary")

#     # --- Tips Section ---
#     with st.container(border=True):
#         st.subheader("💡 Agricultural Tips")
#         for tip in TIPS:
#             st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)

#     # --- Recommendations Section ---
#     with st.container(border=True):
#         st.subheader("✅ Recommended Crops")

#         if "recommendations" not in st.session_state:
#             st.session_state.recommendations = []

#         if submitted and crop_model:
#             with st.spinner("Analyzing soil and weather conditions..."):
#                 try:
#                     data = {
#                         "nitrogen": n, "phosphorus": p, "potassium": k,
#                         "temperature": temp, "humidity": humidity,
#                         "ph": ph, "rainfall": rainfall
#                     }
#                     features = [list(data.values())]
#                     probabilities = crop_model.predict_proba(features)[0]
#                     crop_probabilities = list(zip(crop_model.classes_, probabilities))
#                     top_crops = sorted(crop_probabilities, key=lambda i: i[1], reverse=True)[:3]

#                     st.session_state.recommendations = []
#                     for crop, confidence in top_crops:
#                         rec_id = db_functions.save_recommendation(data, crop.capitalize())
#                         st.session_state.recommendations.append({
#                             'id': rec_id,
#                             'crop': crop,
#                             'confidence': confidence,
#                             'status': 'new'
#                         })

#                 except Exception as e:
#                     st.error(f"Analysis failed: {str(e)}")

#         # Display recommendations
#         if st.session_state.recommendations:
#             rec_cols = st.columns(3)
#             for i, rec in enumerate(st.session_state.recommendations):
#                 with rec_cols[i]:
#                     is_done = (rec['status'] == 'done')
#                     done_class = "done" if is_done else ""
#                     st.markdown(f'<div class="recommendation-item {done_class}">', unsafe_allow_html=True)

#                     relative_image_path = crop_data.CROP_IMAGES.get(rec['crop'].lower(), crop_data.CROP_IMAGES['default'])
#                     full_image_path = os.path.join(ROOT_DIR, relative_image_path)

#                     if os.path.exists(full_image_path):
#                         st.image(full_image_path, use_container_width=True)
#                     else:
#                         st.info("🌱 Default crop image")

#                     details = crop_data.CROP_DETAILS.get(rec['crop'].lower(), crop_data.CROP_DETAILS['default'])
#                     st.markdown(f"**{rec['crop'].capitalize()}**")
#                     st.markdown(f"*Confidence: {rec['confidence']*100:.1f}%*")
#                     st.markdown(f"{details['description']}")
#                     st.markdown(f"💧 Water: {details['water']} | ⚖️ Yield: {details['yield']}")

#                     if not is_done:
#                         if st.button("Mark as Done", key=f"done_{rec['id']}"):
#                             db_functions.mark_as_done(rec['id'])
#                             st.session_state.recommendations[i]['status'] = 'done'
#                             st.rerun()
#                     else:
#                         st.success("✔️ Done")
#                     st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             st.info("👆 Click 'Get Recommendations' to see suggested crops for your conditions")

# except Exception:
#     st.error("An error occurred on this page")
#     if st.checkbox("Show error details"):
#         st.code(traceback.format_exc())
# ---- pages/2_Recommendations.py ----
import streamlit as st
import joblib
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim
import requests
import sys
import os

# --- Correctly set up the path to import shared files ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
import crop_data
from layout_helper import setup_page, close_page_div

st.set_page_config(page_title="Crop Recommendations", page_icon="✅", layout="wide", initial_sidebar_state="expanded")

# Setup page with consistent layout
setup_page(
    title="Recommendations",
    icon="✅",
    background_image="https://images.unsplash.com/photo-1574943320219-553eb213f72d?q=80&w=2070&auto=format&fit=crop",
    page_class="recommendations-page"
)

# Advanced Premium Background with Multiple Layers and Effects
st.markdown(
    """
    <style>
    /* Keyframes for animated gradient overlay */
    @keyframes gradient-shift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-20px);
        }
    }
    
    /* Main App Background - Multi-layered */
    .stApp {
        position: relative;
        background: #ecfdf5;
        background-attachment: fixed;
    }
    
    /* Create pseudo-element for background image with advanced effects */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        background-image: url("https://images.unsplash.com/photo-1574943320219-553eb213f72d?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.60;
        filter: brightness(1.1) saturate(1.05);
    }
    
    /* Static gradient overlay - No animation */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        background: rgba(236, 253, 245, 0.35);
        pointer-events: none;
    }
    
    /* Alternative targeting for Streamlit container */
    [data-testid="stAppViewContainer"] {
        background: transparent;
        position: relative;
        z-index: 2;
    }
    
    /* Main content area styling */
    .main .block-container {
        background: transparent;
        padding: 2rem 1rem;
        position: relative;
        z-index: 3;
    }
    
    /* Premium Glass Cards with Enhanced Effects - NO BLACK BORDERS */
    div[data-testid="stVerticalBlock"] > div[style*="border"],
    div[data-testid="stExpander"],
    .stForm,
    div[class*="css"],
    section[data-testid="stSidebar"] > div,
    div[data-baseweb="base-input"],
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        border-radius: 1.25rem !important;
        border: none !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.15),
            0 4px 16px rgba(16, 185, 129, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
        position: relative;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Remove ALL default Streamlit borders - Comprehensive */
    div[data-testid="stVerticalBlock"] > div {
        border: none !important;
    }
    
    div[class*="element-container"] {
        border: none !important;
    }
    
    /* Remove borders from all containers */
    div[data-testid="column"],
    div[data-testid="stHorizontalBlock"],
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[style*="border"],
    .row-widget,
    .stMarkdown > div,
    section > div > div {
        border: none !important;
    }
    
    /* Override any inline border styles */
    [style*="border: 1px solid"],
    [style*="border: thin"],
    [style*="border-width: 1px"] {
        border: none !important;
    }
    
    /* Specifically target expander borders */
    div[data-testid="stExpander"] > div,
    div[data-testid="stExpander"] > div > div,
    details,
    summary {
        border: none !important;
        border-top: none !important;
        border-bottom: none !important;
        border-left: none !important;
        border-right: none !important;
    }
    
    /* Remove borders from sections and containers */
    section,
    section > div,
    .element-container,
    .stMarkdown,
    div[data-testid="stMarkdownContainer"] {
        border: none !important;
    }
    
    /* Remove all possible border variations */
    * {
        border-color: transparent !important;
    }
    
    /* Target specific problematic elements */
    div[class*="st-"] {
        border: none !important;
    }
    
    /* Hover effect for cards */
    div[data-testid="stExpander"]:hover {
        transform: translateY(-4px);
        border: none !important;
        box-shadow: 
            0 12px 48px rgba(31, 38, 135, 0.2),
            0 4px 12px rgba(16, 185, 129, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Title - Optimized */
    .stApp h1 {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 2rem 2.5rem;
        border-radius: 1.5rem;
        border: none !important;
        border-left: 6px solid #10b981 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
        color: #111827 !important;
    }
    
    /* Remove animated shine to reduce GPU load */
    .stApp h1::before {
        display: none;
    }
    
    /* Subtitle styling */
    .stApp p[style*="color: #059669"] {
        background: rgba(255, 255, 255, 0.97) !important;
        backdrop-filter: blur(15px);
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        color: #059669 !important;
        font-weight: 600;
    }
    
    /* Regular paragraphs */
    .stApp p {
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(12px);
        padding: 1rem 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        color: #374151 !important;
        line-height: 1.7;
    }
    
    /* Button enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(135deg, #059669, #047857) !important;
    }
    
    /* Input field styling - Optimized */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    input[type="text"],
    input[type="number"],
    textarea,
    .stTextInput > div,
    .stSelectbox > div {
        background: rgba(255, 255, 255, 0.98) !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08) !important;
        transition: box-shadow 0.2s ease !important;
        color: #1f2937 !important;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    input[type="text"]:focus,
    input[type="number"]:focus {
        border: none !important;
        box-shadow: 
            0 0 0 3px rgba(16, 185, 129, 0.2),
            0 6px 20px rgba(16, 185, 129, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.7) !important;
        outline: none !important;
    }
    
    /* Slider enhancements */
    .stSlider {
        background: rgba(255, 255, 255, 0.95) !important;
        padding: 1rem;
        border-radius: 0.75rem;
    }
    
    .stSlider > div > div > div {
        background: rgba(209, 250, 229, 0.8) !important;
    }
    
    /* Map container */
    iframe {
        border-radius: 1rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15) !important;
        border: 3px solid rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Label text enhancement */
    label {
        color: #111827 !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
    }
    
    /* Agricultural Tips Section - Optimized */
    .stApp h2,
    .stApp h3 {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1.5rem 2rem;
        border-radius: 1.25rem;
        border: none !important;
        border-left: 6px solid #10b981 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        color: #111827 !important;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    
    /* Tips content container - Optimized */
    .stApp ul,
    .stApp ol {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 2rem 2rem 2rem 3.5rem !important;
        border-radius: 1.25rem;
        border: none !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        margin: 0.5rem 0 2rem 0 !important;
    }
    
    .stApp ul li,
    .stApp ol li {
        color: #111827 !important;
        font-size: 1rem;
        line-height: 2;
        margin-bottom: 1rem;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
        font-weight: 500;
    }
    
    .stApp ul li strong,
    .stApp ol li strong {
        color: #059669 !important;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Icon styling in tips */
    .stApp ul li::marker,
    .stApp ol li::marker {
        color: #10b981 !important;
        font-weight: bold;
    }
    
    /* Decorative elements - Disabled to reduce GPU load */
    /* Animation removed for better performance */
    
    /* ===== CUSTOM MINIMAL SCROLLBAR ===== */
    
    /* Scrollbar styling for Chrome, Safari and Opera */
    body::-webkit-scrollbar,
    html::-webkit-scrollbar,
    .main::-webkit-scrollbar,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar,
    [data-testid="stAppViewContainer"] > .main::-webkit-scrollbar,
    section::-webkit-scrollbar,
    .stApp::-webkit-scrollbar,
    *::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    body::-webkit-scrollbar-track,
    html::-webkit-scrollbar-track,
    .main::-webkit-scrollbar-track,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-track,
    [data-testid="stAppViewContainer"] > .main::-webkit-scrollbar-track,
    section::-webkit-scrollbar-track,
    .stApp::-webkit-scrollbar-track,
    *::-webkit-scrollbar-track {
        background: rgba(16, 185, 129, 0.05) !important;
        border-radius: 10px !important;
    }
    
    body::-webkit-scrollbar-thumb,
    html::-webkit-scrollbar-thumb,
    .main::-webkit-scrollbar-thumb,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb,
    [data-testid="stAppViewContainer"] > .main::-webkit-scrollbar-thumb,
    section::-webkit-scrollbar-thumb,
    .stApp::-webkit-scrollbar-thumb,
    *::-webkit-scrollbar-thumb {
        background: rgba(16, 185, 129, 0.3) !important;
        border-radius: 10px !important;
        transition: background 0.3s ease;
    }
    
    body::-webkit-scrollbar-thumb:hover,
    html::-webkit-scrollbar-thumb:hover,
    .main::-webkit-scrollbar-thumb:hover,
    [data-testid="stAppViewContainer"]::-webkit-scrollbar-thumb:hover,
    [data-testid="stAppViewContainer"] > .main::-webkit-scrollbar-thumb:hover,
    section::-webkit-scrollbar-thumb:hover,
    .stApp::-webkit-scrollbar-thumb:hover,
    *::-webkit-scrollbar-thumb:hover {
        background: rgba(16, 185, 129, 0.5) !important;
    }
    
    /* Scrollbar for Firefox */
    body,
    html,
    .main,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main,
    section,
    .stApp,
    * {
        scrollbar-width: thin !important;
        scrollbar-color: rgba(16, 185, 129, 0.3) rgba(16, 185, 129, 0.05) !important;
    }
    
    /* Ensure smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* ===== FIX INFINITE SCROLL ISSUE ===== */
    
    /* Prevent scroll beyond content */
    body,
    html {
        overflow-x: hidden !important;
        height: auto !important;
        max-height: 100% !important;
    }
    
    /* Main container height fix */
    [data-testid="stAppViewContainer"],
    .main {
        min-height: 100vh !important;
        height: auto !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }
    
    /* Block container */
    .main .block-container {
        max-width: 100%;
        padding-bottom: 5rem !important;
    }
    
    /* Prevent overscroll */
    body {
        overscroll-behavior: none;
        position: relative;
    }
    
    /* Remove extra bottom space */
    .main > div:last-child {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Crop Cards Grid Layout */
    div[data-testid="column"] {
        padding: 0.5rem !important;
    }
    
    /* Crop Card Container Alignment */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem !important;
        align-items: stretch !important;
    }
    
    /* Individual Crop Cards */
    div[data-testid="column"] > div {
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    /* Crop Card Styling */
    .element-container {
        width: 100% !important;
    }
    
    /* Ensure consistent card heights */
    div[data-testid="stVerticalBlock"] {
        height: 100%;
    }
    
    /* Remove any extra margins */
    .row-widget {
        margin: 0 !important;
    }
    
    /* Column alignment */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: stretch;
    }
    
    /* Card image container */
    .stImage {
        border-radius: 1rem 1rem 0 0 !important;
        overflow: hidden;
    }
    
    /* Crop name and details */
    .stMarkdown h3,
    .stMarkdown h4 {
        margin: 0.5rem 0 !important;
        padding: 0.5rem 1rem !important;
    }
    
    /* "Mark as Done" buttons alignment */
    .stButton {
        width: 100%;
        margin-top: auto;
    }
    
    .stButton > button {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# # --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# Use the shared sidebar and header components for consistency
# authenticated_sidebar()
# custom_header("Recommendations")

TIPS = [
    "**Soil Testing:** Regularly test your soil to understand its nutrient profile and pH level for accurate recommendations.",
    "**Crop Rotation:** Avoid planting the same crop in the same place year after year to manage pests and improve soil health.",
    "**Water Management:** Use efficient irrigation methods like drip irrigation to conserve water.",
    "**Integrated Pest Management (IPM):** Combine biological, cultural, and chemical practices to manage pests sustainably."
]

def get_weather(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5).json()
        return {"temperature": response["main"]["temp"], "humidity": response["main"]["humidity"]}
    except Exception:
        st.warning("Could not fetch live weather data. Using default values.")
        return {"temperature": 25.0, "humidity": 70.0}

try:
    # Construct the correct, absolute path to the model file from the root
    model_path = os.path.join(ROOT_DIR, 'crop_model.joblib')
    crop_model = joblib.load(model_path)
except Exception:
    st.error("crop_model.joblib not found in the main project folder.")
    crop_model = None

st.title("🌾 Crop Recommendation Tool")
st.markdown(
    "<p style='font-size: 1.1rem; color: #059669; margin-bottom: 2rem; font-weight: 500;'>"
    "Get AI-powered crop recommendations based on soil conditions, weather, and location data.</p>",
    unsafe_allow_html=True
)

with st.expander("🔎 Explore Crops by Season or Type"):
    col1, col2 = st.columns(2)
    with col1:
        season = st.selectbox("Filter by Season", options=list(crop_data.CROP_FILTER_DATA['seasons'].keys()))
        st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['seasons'][season])}</div>", unsafe_allow_html=True)
    with col2:
        crop_type = st.selectbox("Filter by Type", options=list(crop_data.CROP_FILTER_DATA['types'].keys()))
        st.markdown(f"<div class='crop-list'>{' | '.join(crop_data.CROP_FILTER_DATA['types'][crop_type])}</div>", unsafe_allow_html=True)

# --- Location Selection Card ---
with st.container(border=True):
    st.subheader("📍 Location Selection")
    
    # Initialize session state
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'lat' not in st.session_state: 
        st.session_state.lat, st.session_state.lon = 12.9716, 77.5946
    if 'selected_location_name' not in st.session_state:
        st.session_state.selected_location_name = ""

    # Show current selected location
    if st.session_state.selected_location_name:
        st.info(f"📍 **Selected:** {st.session_state.selected_location_name}")
    
    search_query = st.text_input("Search for a location", placeholder="Enter city, address, or coordinates")
    
    # Handle search submission only on Enter
    if search_query and search_query != st.session_state.get('last_search', ''):
        st.session_state.last_search = search_query
        try:
            geolocator = Nominatim(user_agent="crop_recommender")
            location = geolocator.geocode(search_query)
            if location: 
                st.session_state.lat, st.session_state.lon = location.latitude, location.longitude
                st.session_state.selected_location_name = location.address
                st.success("✅ Location found!")
            else:
                st.warning("⚠️ Location not found. Try a different search.")
        except Exception as e: 
            st.error(f"Geocoding failed: {str(e)}")

    # Create the map
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=10)
    folium.Marker([st.session_state.lat, st.session_state.lon]).add_to(m)
    
    # Store previous coordinates to detect actual changes
    if 'prev_lat' not in st.session_state:
        st.session_state.prev_lat = st.session_state.lat
        st.session_state.prev_lon = st.session_state.lon
    
    map_data = st_folium(m, height=350, use_container_width=True, key="map")
    
    # Handle map click - only update if coordinates actually changed
    if map_data and map_data.get("last_clicked"):
        clicked_lat, clicked_lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
        
        # Check if coordinates changed significantly (avoid float precision issues)
        lat_changed = abs(st.session_state.prev_lat - clicked_lat) > 0.0001
        lon_changed = abs(st.session_state.prev_lon - clicked_lon) > 0.0001
        
        if lat_changed or lon_changed:
            st.session_state.lat, st.session_state.lon = clicked_lat, clicked_lon
            st.session_state.prev_lat, st.session_state.prev_lon = clicked_lat, clicked_lon
            
            # Reverse geocode to get location name
            try:
                geolocator = Nominatim(user_agent="crop_recommender")
                location = geolocator.reverse(f"{clicked_lat}, {clicked_lon}", exactly_one=True, timeout=5)
                if location and location.address:
                    st.session_state.selected_location_name = location.address
                else:
                    st.session_state.selected_location_name = f"{clicked_lat:.4f}, {clicked_lon:.4f}"
            except Exception:
                st.session_state.selected_location_name = f"{clicked_lat:.4f}, {clicked_lon:.4f}"
            
            st.rerun()

# --- Input Parameters Card ---
weather_data = get_weather(st.session_state.lat, st.session_state.lon)

# Initialize session state for input parameters
if 'n_value' not in st.session_state: st.session_state.n_value = 50
if 'p_value' not in st.session_state: st.session_state.p_value = 50
if 'k_value' not in st.session_state: st.session_state.k_value = 50
if 'temp_value' not in st.session_state: st.session_state.temp_value = max(8.0, min(50.0, float(weather_data["temperature"])))
if 'humidity_value' not in st.session_state: st.session_state.humidity_value = max(14.0, min(100.0, float(weather_data["humidity"])))
if 'ph_value' not in st.session_state: st.session_state.ph_value = 6.5
if 'rainfall_value' not in st.session_state: st.session_state.rainfall_value = 100.0

with st.container(border=True):
    st.subheader("🧪 Input Parameters")
    form_col1, form_col2 = st.columns(2)
    with form_col1:
        n = st.slider("Nitrogen (N)", 0, 140, st.session_state.n_value, step=1, key="n_slider")
        p = st.slider("Phosphorus (P)", 5, 145, st.session_state.p_value, step=1, key="p_slider")
        k = st.slider("Potassium (K)", 5, 205, st.session_state.k_value, step=1, key="k_slider")
    with form_col2:
        temp_val = max(8.0, min(50.0, float(weather_data["temperature"])))
        hum_val = max(14.0, min(100.0, float(weather_data["humidity"])))
        temp = st.slider("Temperature (°C)", 8.0, 50.0, st.session_state.temp_value, step=0.1, key="temp_slider")
        humidity = st.slider("Humidity (%)", 14.0, 100.0, st.session_state.humidity_value, step=0.1, key="humidity_slider")
        ph = st.slider("Soil pH", 3.5, 9.9, st.session_state.ph_value, step=0.1, key="ph_slider")
    rainfall = st.slider("Rainfall (mm)", 20.0, 300.0, st.session_state.rainfall_value, step=0.1, key="rainfall_slider")
    submitted = st.button("Get Recommendations")
    
    # Update session state when sliders change
    st.session_state.n_value = n
    st.session_state.p_value = p
    st.session_state.k_value = k
    st.session_state.temp_value = temp
    st.session_state.humidity_value = humidity
    st.session_state.ph_value = ph
    st.session_state.rainfall_value = rainfall

# --- Tips Section ---
with st.container(border=True):
    st.subheader("💡 Agricultural Tips")
    for tip in TIPS: st.markdown(f"<div class='tip-item'>{tip}</div>", unsafe_allow_html=True)

# --- Recommended Crops Card (at the bottom) ---
with st.container(border=True):
    st.subheader("✅ Recommended Crops")
    if "recommendations" not in st.session_state: st.session_state.recommendations = []
    
    if submitted:
        if not crop_model:
            st.error("❌ Model not loaded. Cannot generate recommendations.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    data = {"nitrogen": n, "phosphorus": p, "potassium": k, "temperature": temp, "humidity": humidity, "ph": ph, "rainfall": rainfall}
                    features = [list(data.values())]
                    probabilities = crop_model.predict_proba(features)[0]
                    crop_probabilities = list(zip(crop_model.classes_, probabilities))
                    top_crops = sorted(crop_probabilities, key=lambda i: i[1], reverse=True)[:3]
                    st.session_state.recommendations = []
                    for crop, confidence in top_crops:
                        try:
                            rec_id = db_functions.save_recommendation(data, crop.capitalize())
                        except Exception as db_err:
                            st.warning(f"Could not save recommendation: {db_err}")
                            rec_id = None
                        st.session_state.recommendations.append({'id': rec_id, 'crop': crop, 'confidence': confidence, 'status': 'new'})
                    st.success("✅ Recommendations generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error generating recommendations: {str(e)}")
                    st.session_state.recommendations = []
    
    if st.session_state.recommendations:
        rec_cols = st.columns(3)
        for i, rec in enumerate(st.session_state.recommendations):
            with rec_cols[i]:
                is_done = (rec['status'] == 'done')
                done_class = "done" if is_done else ""
                st.markdown(f'<div class="recommendation-item {done_class}">', unsafe_allow_html=True)
                
                relative_image_path = crop_data.CROP_IMAGES.get(rec['crop'].lower(), crop_data.CROP_IMAGES['default'])
                full_image_path = os.path.join(ROOT_DIR, relative_image_path)
                
                if os.path.exists(full_image_path):
                    st.image(full_image_path)
                else:
                    st.warning(f"Image not found")

                details = crop_data.CROP_DETAILS.get(rec['crop'].lower(), crop_data.CROP_DETAILS.get('default', {'description': 'N/A', 'water': 'N/A', 'yield': 'N/A'}))
                st.markdown(f"**{rec['crop'].capitalize()}**")
                st.markdown(f"<small>Confidence: {rec['confidence']*100:.1f}%</small>", unsafe_allow_html=True)
                st.markdown(f"<small>{details['description']}</small>", unsafe_allow_html=True)
                st.markdown(f"<small>💧 Water: {details['water']} | ⚖️ Yield: {details['yield']}</small>", unsafe_allow_html=True)
                if not is_done:
                    # Only show button if rec_id is valid
                    if rec.get('id'):
                        if st.button("Mark as Done", key=f"done_{rec['id']}"):
                            try:
                                db_functions.mark_as_done(rec['id'])
                                st.session_state.recommendations[i]['status'] = 'done'
                                st.rerun()
                            except Exception as e:
                                st.error(f"Could not mark as done: {e}")
                    else:
                        st.info("ℹ️ Not saved to database")
                else:
                    st.success("✔️ Done")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Results will appear here.")

# Close the recommendations-page div
st.markdown('</div>', unsafe_allow_html=True)

