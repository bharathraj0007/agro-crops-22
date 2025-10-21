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
    background_image="https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=2070&auto=format&fit=crop",
    page_class="profile-page"
)

# Page-specific styling
st.markdown(
    """
    <style>
    /* Profile Header Styling */
    .profile-header {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        padding: 3rem 2rem !important;
        border-radius: 1.5rem !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
        text-align: center;
        margin-bottom: 2rem;
        border: none !important;
    }
    
    .profile-header h1 {
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        border: none !important;
        color: white !important;
        margin: 0.5rem 0 !important;
    }
    
    .profile-header p {
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    
    /* Stat Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(16, 185, 129, 0.2);
    }
    
    .stat-card h3 {
        background: none !important;
        padding: 0 !important;
        margin: 0.5rem 0 !important;
        box-shadow: none !important;
        border: none !important;
        color: #10b981 !important;
        font-size: 1.8rem !important;
    }
    
    .stat-card p {
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        color: #6b7280;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Section Cards */
    .section-card {
        background: rgba(255, 255, 255, 0.98);
        padding: 1.5rem;
        border-radius: 1.25rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .section-card h3 {
        background: none !important;
        padding: 0 !important;
        margin: 0 0 1rem 0 !important;
        box-shadow: none !important;
        border: none !important;
        color: #10b981 !important;
    }
    
    .section-card p, .section-card ul {
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        color: #374151;
    }
    
    .section-card ul {
        padding-left: 1.5rem !important;
    }
    
    .section-card li {
        margin: 0.5rem 0;
        color: #374151;
    }
    
    /* Form Section Headings */
    .stForm h3 {
        background: none !important;
        padding: 0 !important;
        margin: 1rem 0 0.5rem 0 !important;
        box-shadow: none !important;
        border: none !important;
        border-left: 4px solid #10b981 !important;
        padding-left: 1rem !important;
        color: #111827 !important;
    }
    
    /* Column spacing */
    div[data-testid="column"] {
        padding: 0.5rem;
    }
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
if 'profile_farm_size' not in st.session_state:
    st.session_state.profile_farm_size = ""
if 'profile_location' not in st.session_state:
    st.session_state.profile_location = ""
if 'profile_irrigation' not in st.session_state:
    st.session_state.profile_irrigation = "Drip Irrigation"

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

# Profile stats with proper containers
col1, col2, col3, col4 = st.columns(4)
role = st.session_state.get('role', 'User')

with col1:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎯</div>
                <h3 style="margin: 0.5rem 0; color: #10b981; background: none !important; padding: 0 !important; box-shadow: none !important; border: none !important;">{total_recs}</h3>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem; background: none !important; padding: 0 !important; box-shadow: none !important;">Total Recommendations</p>
            </div>
            """,
            unsafe_allow_html=True
        )
with col2:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🌾</div>
                <h3 style="margin: 0.5rem 0; color: #10b981; background: none !important; padding: 0 !important; box-shadow: none !important; border: none !important;">{unique_crops}</h3>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem; background: none !important; padding: 0 !important; box-shadow: none !important;">Unique Crops Tried</p>
            </div>
            """,
            unsafe_allow_html=True
        )
with col3:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏆</div>
                <h3 style="margin: 0.5rem 0; color: #10b981; background: none !important; padding: 0 !important; box-shadow: none !important; border: none !important;">Active</h3>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem; background: none !important; padding: 0 !important; box-shadow: none !important;">Account Status</p>
            </div>
            """,
            unsafe_allow_html=True
        )
with col4:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 0.5rem;">👤</div>
                <h3 style="margin: 0.5rem 0; color: #10b981; background: none !important; padding: 0 !important; box-shadow: none !important; border: none !important;">{role}</h3>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem; background: none !important; padding: 0 !important; box-shadow: none !important;">User Role</p>
            </div>
            """,
            unsafe_allow_html=True
        )

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

# Quick Actions Section
with st.container(border=True):
    st.markdown("### 🌿 Quick Actions")
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        if st.button("🌾 View Recommendations", use_container_width=True):
            st.switch_page("pages/2_Recommendations.py")
    with col_btn2:
        if st.button("📊 View Insights", use_container_width=True):
            st.switch_page("pages/3_Insights.py")
    with col_btn3:
        if st.button("📜 View History", use_container_width=True):
            st.switch_page("pages/4_History.py")

st.markdown("<br>", unsafe_allow_html=True)

# Profile Form - Single Column Layout
with st.container(border=True):
    st.markdown("## 📝 Farm Profile")
    st.markdown("---")
    
    with st.form("profile_form"):
        # Basic Farm Information
        st.markdown("### 🏞️ Basic Information")
        
        col1, col2 = st.columns(2)
        with col1:
            farm_location = st.text_input(
                "Farm Location *",
                value=st.session_state.profile_location,
                placeholder="e.g., Bangalore Rural, Karnataka",
                help="Enter your farm's location (city, district, state)",
                key="profile_location_input"
            )
        with col2:
            farm_size = st.text_input(
                "Farm Size",
                value=st.session_state.profile_farm_size,
                placeholder="e.g., 5 acres, 2 hectares",
                help="Enter the size of your farm",
                key="profile_farm_size_input"
            )
        
        farm_info = st.text_area(
            "Farm Description",
            value=st.session_state.profile_farm_info,
            placeholder="Describe your farm: main crops, farming experience, challenges, etc.",
            height=100,
            help="Provide additional details about your farm",
            key="profile_farm_info_input"
        )
        
        st.markdown("---")
        
        # Soil and Irrigation
        st.markdown("### 🧩 Soil & Irrigation Details")
        
        col1, col2 = st.columns(2)
        with col1:
            soil_options = ["Loamy", "Sandy", "Clay", "Silty", "Peaty", "Chalky", "Black Soil", "Red Soil", "Alluvial"]
            try:
                current_soil_index = soil_options.index(st.session_state.profile_soil_type)
            except ValueError:
                current_soil_index = 0
                
            soil_type = st.selectbox(
                "Primary Soil Type *",
                options=soil_options,
                index=current_soil_index,
                help="Select the predominant soil type on your farm",
                key="profile_soil_type_input"
            )
        
        with col2:
            irrigation_options = [
                "Drip Irrigation",
                "Sprinkler Irrigation", 
                "Flood Irrigation",
                "Furrow Irrigation",
                "Rain-fed",
                "Mixed Methods",
                "Other"
            ]
            try:
                current_irrigation_index = irrigation_options.index(st.session_state.profile_irrigation)
            except ValueError:
                current_irrigation_index = 0
                
            irrigation_type = st.selectbox(
                "Irrigation Method",
                options=irrigation_options,
                index=current_irrigation_index,
                help="Select your primary irrigation method",
                key="profile_irrigation_input"
            )
        
        st.markdown("---")
        
        # Farming Preferences
        st.markdown("### ⚙️ Farming Preferences & Practices")
        
        preferences = st.text_area(
            "Your Farming Philosophy",
            value=st.session_state.profile_preferences,
            placeholder="e.g., Organic farming, water conservation, sustainable practices, crop rotation, etc.",
            height=100,
            help="Share your farming philosophy, preferences, and practices",
            key="profile_preferences_input"
        )
        
        st.markdown("---")
        st.caption("* Required fields")
        
        # Form buttons
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 1])
        with col_btn1:
            st.markdown("")  # Spacer
        with col_btn2:
            reset = st.form_submit_button("🔄 Reset", use_container_width=True, type="secondary")
        with col_btn3:
            submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        if submitted:
            # Validate required fields
            if not farm_location:
                st.error("❌ Please enter your farm location.")
            else:
                # Update session state with form values
                st.session_state.profile_farm_info = farm_info
                st.session_state.profile_soil_type = soil_type
                st.session_state.profile_preferences = preferences
                st.session_state.profile_farm_size = farm_size
                st.session_state.profile_location = farm_location
                st.session_state.profile_irrigation = irrigation_type
                
                db_functions.save_profile_data(farm_info, soil_type, preferences)
                st.success("✅ Your profile has been saved successfully!")
                st.balloons()
                st.rerun()
        elif reset:
            # Reset session state to default values
            st.session_state.profile_farm_info = profile_data.get('farm_info', '')
            st.session_state.profile_soil_type = profile_data.get('soil_type', 'Loamy')
            st.session_state.profile_preferences = profile_data.get('preferences', '')
            st.session_state.profile_farm_size = ""
            st.session_state.profile_location = ""
            st.session_state.profile_irrigation = "Drip Irrigation"
            st.info("🔄 Form has been reset to default values.")
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Profile Tips Card
with st.container(border=True):
    st.markdown("### 💡 Profile Tips")
    st.markdown("---")
    
    col_tip1, col_tip2 = st.columns(2)
    with col_tip1:
        st.markdown("**🎯 Why complete your profile?**")
        st.markdown("""
        - Get personalized recommendations
        - Track your farming journey
        - Better insights and analytics
        - Connect with similar farmers
        """)
    with col_tip2:
        st.markdown("**🔒 Privacy & Security**")
        st.markdown("""
        - Data stored locally
        - Never shared without consent
        - Full control over your info
        - Secure and encrypted
        """)
    st.caption("💡 Keep your profile updated for the best experience!")

# Footer spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Close page wrapper
close_page_div()

