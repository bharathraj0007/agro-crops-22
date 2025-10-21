# ---- pages/7_Admin_Dashboard.py ----
import streamlit as st
import sys
import os

# --- Correctly set up the path to import shared files ---
# This script is in the 'pages' folder, so we go up one level to the root
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
import header
from sidebar import authenticated_sidebar

st.set_page_config(page_title="Admin Dashboard", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

def load_css(file_name):
    # Correct path to find style.css from the pages subfolder
    css_path = os.path.join(ROOT_DIR, file_name)
    with open(css_path) as f: 
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# --- Authentication & Role Check ---
# This ensures only logged-in admins can see this page
if not st.session_state.get('logged_in') or st.session_state.get('role') != 'Admin':
    st.error("You do not have permission to access this page.")
    st.page_link("app.py", label="Go back to Login")
    st.stop()

# Use the shared sidebar and header components for consistency
authenticated_sidebar()
header.custom_header("Admin Dashboard")

st.title(f"👑 Admin Dashboard")
st.markdown(f"Welcome, {st.session_state['username']}! This is the central control panel.")

# --- Admin Stats ---
try:
    admin_stats = db_functions.get_admin_stats()
    col1, col2 = st.columns(2)
    col1.metric(label="Total Recommendations in System", value=admin_stats['total_recommendations'])
    col2.metric(label="Total User Profiles", value=admin_stats['total_profiles'])
except Exception as e:
    st.error(f"Failed to load admin statistics: {e}")

st.markdown("---")
st.subheader("Recent Activity")
# In future steps, we can add a log of recent recommendations or signups here.
st.info("A log of recent system activity will be displayed here in a future update.")

# The logout button is now handled by the authenticated_sidebar component