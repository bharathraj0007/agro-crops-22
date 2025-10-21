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
    # Profile Tips Card
    with st.container(border=True):
        st.markdown("### 💡 Profile Tips")
        st.markdown("---")
        st.markdown("**🎯 Why complete your profile?**")
        st.markdown("""
        - Get personalized recommendations
        - Track your farming journey
        - Better insights and analytics
        - Connect with similar farmers
        """)
        st.markdown("**🔒 Privacy Notice:**")
        st.caption("Your profile data is stored locally and never shared without your consent.")
    
    # Quick Actions Card
    with st.container(border=True):
        st.markdown("### 🌿 Quick Actions")
        st.markdown("---")
        if st.button("🌾 View Recommendations", use_container_width=True):
            st.switch_page("pages/2_Recommendations.py")
        if st.button("📊 View Insights", use_container_width=True):
            st.switch_page("pages/3_Insights.py")
        if st.button("📜 View History", use_container_width=True):
            st.switch_page("pages/4_History.py")

# Footer spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Close page wrapper
close_page_div()

