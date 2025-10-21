# ---- pages/1_Dashboard.py ----
import streamlit as st
import sys
import os
import datetime
import pandas as pd
import requests

# --- Path setup ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

# Initialize page config
st.set_page_config(
    page_title="AgriAssist Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

import db_functions
from translations import get_text, get_language_switcher
from header import custom_header
from layout_helper import setup_page, close_page_div
from sidebar import authenticated_sidebar

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'dashboard_preferences' not in st.session_state:
    st.session_state.dashboard_preferences = {}

# Setup page with consistent layout
setup_page(
    title="Dashboard",
    icon="🌱",
    background_image="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2070&auto=format&fit=crop",
    page_class="dashboard-page"
)

# Set custom styles for metrics
st.markdown("""
    <style>
    /* Custom metric card styling */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    div[data-testid="stMetric"] > div {
        padding: 0 !important;
    }
    
    div[data-testid="stMetric"] > div > div {
        margin: 0 !important;
    }
    
    div[data-testid="stMetric"] > div > div[data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #6c757d;
        margin-bottom: 0.5rem !important;
    }
    
    div[data-testid="stMetric"] > div > div[data-testid="stMetricValue"] > div {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #2b9348 !important;
    }
    
    /* Custom card styling */
    .custom-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    .card-title {
        color: #1b5e20;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .card-title i {
        font-size: 1.3rem;
    }
    
    /* Custom tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre;
        background-color: #f8f9fa;
        border-radius: 8px 8px 0 0;
        gap: 1rem;
        padding: 0 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2b9348;
        color: white;
    }
    
    /* Custom buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:first-child {
        background-color: #2b9348;
        border: none;
    }
    
    .stButton > button:first-child:hover {
        background-color: #1b5e20;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for enhanced dashboard design
st.markdown("""
<style>
/* Background Image for Dashboard */
.stApp {
    background-image: linear-gradient(rgba(255, 255, 255, 0.40), rgba(255, 255, 255, 0.40)), 
                      url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2232&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
}

.main {
    background: transparent;
}

/* Dashboard-specific styles */
.dashboard-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 1rem;
}

/* News Cards */
.news-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    border-left: 4px solid #2b9348;
    height: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    position: relative;
    overflow: hidden;
}

.news-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #2b9348 0%, #55a630 100%);
    transition: width 0.3s ease;
}

.news-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(43, 147, 72, 0.15);
}

.news-card:hover::before {
    width: 6px;
}

.news-card h4 { 
    margin: 0 0 0.75rem 0;
    color: #1b5e20;
    font-size: 1.05rem;
    font-weight: 700;
    line-height: 1.4;
}

.news-card p { 
    margin: 0 0 0.5rem 0;
    color: #4a4a4a;
    line-height: 1.6;
    font-size: 0.9rem;
}

.news-date {
    font-size: 0.8rem;
    color: #6b7280;
    font-weight: 500;
    display: block;
    margin-top: 0.75rem;
    padding-top: 0.5rem;
    border-top: 1px solid #f3f4f6;
}

/* Enhanced Metric Cards */
.metric-card {
    background: linear-gradient(135deg, white 0%, #f9fafb 100%);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    margin-top: 1.5rem;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2b9348 0%, #55a630 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(43, 147, 72, 0.15);
    border-color: #2b9348;
}

.metric-card:hover::after {
    opacity: 1;
}

.metric-card h3 {
    font-size: 0.85rem;
    color: #6b7280;
    margin-bottom: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-card p {
    font-size: 2.25rem;
    font-weight: 800;
    background: linear-gradient(135deg, #2b9348 0%, #1b5e20 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
}

/* Enhanced Feature Cards */
.feature-section {
    margin-top: 3rem;
}

.feature-card-wrapper {
    height: 100%;
}

.image-card {
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
    text-align: center;
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.image-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(43, 147, 72, 0.15);
    border-color: #2b9348;
}

.image-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 1rem;
}

.image-card h3 {
    margin: 0.5rem 0 0.75rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: #1b5e20;
}

.image-card p {
    color: #4a4a4a;
    line-height: 1.6;
    font-size: 0.9rem;
    margin: 0;
    flex: 1;
}

/* Section Headers */
.section-header {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 2.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid #2b9348;
    display: block;
    width: 100%;
}

/* Divider: make invisible but keep spacing */
.custom-divider {
    height: 0;
    margin: 2rem 0; /* keep vertical space between sections */
    border: none;
    background: transparent;
    box-shadow: none;
}

/* Remove any default horizontal rules */
hr {
    border: none !important;
    height: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
    margin: 2rem 0 !important; /* retain spacing if any hr is present */
}

/* Section content spacing */
.section-content {
    margin-top: 1.25rem;
}

/* Today Highlights Cards */
.highlight-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 1.25rem 1.25rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    margin-top: 1rem;
}
.highlight-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 26px rgba(43,147,72,0.18);
    border-color: #cde7d4;
}
.highlight-card h4 {
    margin: 0 0 0.5rem 0;
    font-size: 1.05rem;
    color: #14532d;
}
.highlight-card p {
    margin: 0;
    color: #374151;
}

/* Subtle pill divider under header */
.section-header + .section-content::before {
    content: '';
    display: block;
    height: 6px;
    width: 120px;
    border-radius: 9999px;
    background: linear-gradient(90deg, #2b9348, #55a630);
    opacity: 0.35;
    margin-bottom: 0.75rem;
}

</style>
""", unsafe_allow_html=True)

# --- Auth Check ---
if not st.session_state.get('logged_in'):
    st.error("You need to be logged in to access this page.")
    st.page_link("app.py", label="Go to Login Page")
    st.stop()

# --- Use Shared Sidebar ---
authenticated_sidebar()

# --- HERO SECTION ---
st.markdown("""
<div class="hero-section" style="
    background-image: linear-gradient(rgba(43, 147, 72, 0.85), rgba(27, 94, 32, 0.9)), 
                      url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2070&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
">
  <h1>🌾 Welcome to AgriAssist</h1>
  <p>Smart crop insights powered by AI — helping farmers grow better, every season.</p>
</div>
""", unsafe_allow_html=True)

# --- Stats Section ---
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

try:
    stats = db_functions.get_dashboard_stats()
    st.markdown('<h2 class="section-header">📊 Quick Stats</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    metrics = [
        ("📊 Total Recommendations", stats['total']),
        ("🌱 Unique Crops", stats['unique_crops']),
        ("🕒 Last Recommendation", stats['latest'])
    ]
    for i, (label, val) in enumerate(metrics):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{label}</h3>
                <p>{val}</p>
            </div>
            """, unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Could not load dashboard stats. Error: {e}")

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# --- Seasonal Highlights ---
def get_current_season():
    m = datetime.datetime.now().month
    if 6 <= m <= 10: return "Kharif Season (Monsoon)", "Rice, Maize, Cotton", "🌧️"
    elif 11 <= m or m <= 3: return "Rabi Season (Winter)", "Wheat, Mustard, Barley", "❄️"
    else: return "Zaid Season (Summer)", "Watermelon, Muskmelon", "☀️"

def get_weather_alert(lat, lon):
    try:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric",
            timeout=5
        ).json()
        desc = res['weather'][0]['description'].capitalize()
        temp = res['main']['temp']
        return f"{desc}, {temp}°C", "☁️"
    except:
        return "Weather data unavailable", "⚠️"

season, crops, icon = get_current_season()
weather, w_icon = get_weather_alert(12.9716, 77.5946)

# News Highlights
st.markdown('<h2 class="section-header">📰 Latest Agricultural News</h2>', unsafe_allow_html=True)
st.markdown('<p style="color: #6b7280; margin-bottom: 1.5rem;">Stay updated with the latest developments in agriculture</p>', unsafe_allow_html=True)

# Create columns for news cards
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container():
        st.markdown("""
        <div class="news-card">
            <h4>🌱 Government Announces New Subsidy for Organic Farming</h4>
            <p>The government has launched a new scheme providing 50% subsidy on organic farming inputs. Farmers can apply through the Kisan Portal starting next month.</p>
            <span class="news-date">Oct 10, 2025</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown("""
        <div class="news-card">
            <h4>🌧️ Monsoon Update: Above Average Rainfall Expected</h4>
            <p>IMD predicts 105% of average rainfall this season, bringing relief to farmers across the country. Experts advise proper water management.</p>
            <span class="news-date">Oct 8, 2025</span>
        </div>
        """, unsafe_allow_html=True)

with col3:
    with st.container():
        st.markdown("""
        <div class="news-card">
            <h4>🌾 New High-Yield Wheat Variety Developed</h4>
            <p>Agricultural scientists have developed a drought-resistant wheat variety that promises 20% higher yields. Field trials show promising results in arid regions.</p>
            <span class="news-date">Oct 5, 2025</span>
        </div>
        """, unsafe_allow_html=True)

# Today's Highlights section
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">🌤️ Today\'s Highlights</h2>', unsafe_allow_html=True)

st.markdown('<div class="section-content">', unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown(f"""
    <div class="highlight-card">
        <h4>🌧️ {season}</h4>
        <p><strong>Recommended Crops:</strong> {crops}</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="highlight-card">
        <h4>☁️ Weather Update</h4>
        <p>{weather}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# --- Feature Section ---
st.markdown('<div class="feature-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">🚀 Explore Our Features</h2>', unsafe_allow_html=True)
st.markdown('<p style="color: #6b7280; margin-bottom: 2rem;">Discover powerful tools designed to help you make better farming decisions</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.markdown("""
    <div class="image-card">
        <img src="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2070&auto-format&fit=crop">
        <h3>Smart Recommendations</h3>
        <p>AI-powered crop suggestions tailored to your soil and climate conditions.</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="image-card">
        <img src="https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?q=80&w=2070&auto-format&fit=crop">
        <h3>Data-Driven Insights</h3>
        <p>Analyze historical patterns to optimize your future crop planning.</p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="image-card">
        <img src="https://images.unsplash.com/photo-1492496913980-501348b61469?q=80&w=1974&auto=format&fit=crop">
        <h3>Resource Management</h3>
        <p>Use AI-backed insights to manage resources and maximize yield efficiency.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close feature-section
st.markdown('</div>', unsafe_allow_html=True)  # Close dashboard-container

# --- Footer ---
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #6b7280;">
    <p style="margin: 0; font-size: 0.95rem;">🌾 Built with ❤️ by <strong style="color: #2b9348;">Bharath Raj</strong> | BE CSE | GMIT</p>
</div>
""", unsafe_allow_html=True)
