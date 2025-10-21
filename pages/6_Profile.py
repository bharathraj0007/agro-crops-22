# ---- pages/6_Profile.py ----
import streamlit as st
import sys
import os

# --- Correctly set up the path to import shared files ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
import header
from sidebar import authenticated_sidebar
from layout_helper import setup_page, close_page_div

st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide", initial_sidebar_state="expanded")

# Setup page with consistent layout
setup_page(
    title="Profile",
    icon="👤",
    background_image="https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?q=80&w=2080&auto=format&fit=crop",
    page_class="profile-page"
)

# Add beautiful background image for Profile page
st.markdown(
    """
    <style>
    /* Main App Background for Profile Page - Farmer Portrait Theme */
    .stApp {
        position: relative;
        background: 
            linear-gradient(135deg, rgba(219, 234, 254, 0.90), rgba(191, 219, 254, 0.85)),
            #dbeafe;
        background-attachment: fixed;
    }
    
    /* Background Image Layer - Farmer Theme */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        background-image: url("https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?q=80&w=2080&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.50;
        filter: brightness(1.2) saturate(1.05);
    }
    
    /* Static gradient overlay */
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        background: rgba(219, 234, 254, 0.35);
        pointer-events: none;
    }
    
    /* App View Container */
    [data-testid="stAppViewContainer"] {
        background: transparent;
        position: relative;
        z-index: 2;
    }
    
    /* Main content area */
    .main .block-container {
        background: transparent;
        padding: 2rem 1rem;
        position: relative;
        z-index: 3;
    }
    
    /* Profile Header */
    .profile-header {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.95), rgba(37, 99, 235, 0.95)) !important;
        padding: 3rem 2rem !important;
        border-radius: 1.5rem !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
        text-align: center;
        margin-bottom: 2rem;
        border: none !important;
    }
    
    /* Headings */
    .stApp h2, .stApp h3 {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #3b82f6 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        color: #111827 !important;
        margin-bottom: 1rem;
    }
    
    /* Cards and Containers */
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="stExpander"],
    .stForm {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 1.25rem !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
        padding: 1.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3) !important;
        transition: transform 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.98) !important;
        border: none !important;
        border-radius: 0.75rem !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Stats/Metrics */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: none !important;
    }
    
    /* Remove all borders */
    div[data-testid="stVerticalBlock"] > div,
    section, section > div {
        border: none !important;
    }
    
    /* Custom Scrollbar */
    *::-webkit-scrollbar { width: 8px !important; }
    *::-webkit-scrollbar-track { background: rgba(59, 130, 246, 0.05) !important; border-radius: 10px !important; }
    *::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.3) !important; border-radius: 10px !important; }
    *::-webkit-scrollbar-thumb:hover { background: rgba(59, 130, 246, 0.5) !important; }
    * { scrollbar-width: thin !important; scrollbar-color: rgba(59, 130, 246, 0.3) rgba(59, 130, 246, 0.05) !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# Initialize session state for profile form fields
if 'profile_farm_info' not in st.session_state:
    st.session_state.profile_farm_info = ""
if 'profile_soil_type' not in st.session_state:
    st.session_state.profile_soil_type = "Loamy"
if 'profile_preferences' not in st.session_state:
    st.session_state.profile_preferences = ""

# Use the shared sidebar and header components for consistency
# authenticated_sidebar()
# header.custom_header("Profile")

# Profile header card
username = st.session_state.get('username', 'User')
st.markdown(
    f"""
    <div class="profile-header">
        <div style="font-size: 4rem; margin-bottom: 1rem;">👨‍🌾</div>
        <h1 style="margin: 0; color: white;">Welcome, {username}!</h1>
        <p style="margin: 0.5rem 0 0 0; color: rgba(255,255,255,0.9);">Manage your farm profile and settings</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Profile stats
try:
    history_df = db_functions.get_history()
    total_recs = len(history_df) if not history_df.empty else 0
    unique_crops = history_df['crop'].nunique() if not history_df.empty and 'crop' in history_df.columns else 0
except:
    total_recs = 0
    unique_crops = 0

st.markdown('<div class="profile-stats">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">🎯</div>
            <h3 style="margin: 0.5rem 0; color: var(--primary);">{total_recs}</h3>
            <p style="margin: 0; color: var(--text-light); font-size: 0.9rem;">Total Recommendations</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">🌾</div>
            <h3 style="margin: 0.5rem 0; color: var(--primary);">{unique_crops}</h3>
            <p style="margin: 0; color: var(--text-light); font-size: 0.9rem;">Unique Crops Tried</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div style="font-size: 2rem;">🏆</div>
            <h3 style="margin: 0.5rem 0; color: var(--primary);">Active</h3>
            <p style="margin: 0; color: var(--text-light); font-size: 0.9rem;">Account Status</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col4:
    role = st.session_state.get('role', 'User')
    st.markdown(
        f"""
        <div class="stat-card">
            <div style="font-size: 2rem;">👤</div>
            <h3 style="margin: 0.5rem 0; color: var(--primary);">{role}</h3>
            <p style="margin: 0; color: var(--text-light); font-size: 0.9rem;">User Role</p>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Load existing profile data
profile_data = db_functions.get_profile_data()

# Update session state with existing profile data if not already set
if not st.session_state.profile_farm_info and profile_data['farm_info']:
    st.session_state.profile_farm_info = profile_data['farm_info']
if st.session_state.profile_soil_type == "Loamy" and profile_data['soil_type'] != "Loamy":
    st.session_state.profile_soil_type = profile_data['soil_type']
if not st.session_state.profile_preferences and profile_data['preferences']:
    st.session_state.profile_preferences = profile_data['preferences']

# Profile form in two columns
col1, col2 = st.columns([2, 1])

with col1:
    with st.form("profile_form"):
        st.markdown("### 🏞️ Farm Information")
        farm_info = st.text_area(
            "Farm Description",
            value=st.session_state.profile_farm_info,
            placeholder="Describe your farm: location, size, main crops, etc.",
            height=120,
            help="Provide details about your farm that can help with better recommendations",
            key="profile_farm_info_input"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🧩 Soil Type")
        soil_options = ["Loamy", "Sandy", "Clay", "Silty", "Peaty", "Chalky"]
        # Ensure the index is valid
        try:
            current_soil_index = soil_options.index(st.session_state.profile_soil_type)
        except ValueError:
            current_soil_index = 0 # Default to Loamy if not found
            
        soil_type = st.selectbox(
            "Primary Soil Type",
            options=soil_options,
            index=current_soil_index,
            help="Select the predominant soil type on your farm",
            key="profile_soil_type_input"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Farming Preferences")
        preferences = st.text_area(
            "Your Preferences",
            value=st.session_state.profile_preferences,
            placeholder="e.g., Organic farming, water conservation, sustainable practices...",
            height=100,
            help="Share your farming philosophy and preferences",
            key="profile_preferences_input"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)
        with col_btn2:
            reset = st.form_submit_button("Reset Form", use_container_width=True, type="secondary")
        
        if submitted:
            # Update session state with form values
            st.session_state.profile_farm_info = farm_info
            st.session_state.profile_soil_type = soil_type
            st.session_state.profile_preferences = preferences
            
            db_functions.save_profile_data(farm_info, soil_type, preferences)
            st.success("✅ Your profile has been saved successfully!")
            st.rerun()
        elif reset:
            # Reset session state to default values
            st.session_state.profile_farm_info = profile_data['farm_info']
            st.session_state.profile_soil_type = profile_data['soil_type']
            st.session_state.profile_preferences = profile_data['preferences']
            st.rerun()

with col2:
    st.markdown(
        """
        <div class="section-card">
            <h3>💡 Profile Tips</h3>
            <br>
            <p><strong>🎯 Why complete your profile?</strong></p>
            <ul style="padding-left: 1.5rem;">
                <li>Get personalized recommendations</li>
                <li>Track your farming journey</li>
                <li>Better insights and analytics</li>
                <li>Connect with similar farmers</li>
            </ul>
            <br>
            <p><strong>🔒 Privacy Notice:</strong></p>
            <p style="font-size: 0.9rem; color: var(--text-light);">Your profile data is stored locally and never shared without your consent.</p>
        </div>
        <br>
        <div class="section-card" style="background: linear-gradient(135deg, #f0fdf4, #dcfce7);">
            <h3>🌿 Quick Actions</h3>
            <br>
        """,
        unsafe_allow_html=True
    )
    if st.button("🌾 View Recommendations", use_container_width=True):
        st.switch_page("pages/2_Recommendations.py")
    if st.button("📊 View Insights", use_container_width=True):
        st.switch_page("pages/3_Insights.py")
    if st.button("📜 View History", use_container_width=True):
        st.switch_page("pages/4_History.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Close page wrapper
st.markdown('</div>', unsafe_allow_html=True)

