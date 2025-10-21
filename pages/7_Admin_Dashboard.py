# ---- pages/7_Admin_Dashboard.py ----
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

st.set_page_config(page_title="Admin Dashboard", page_icon="👑", layout="wide", initial_sidebar_state="collapsed")

# Setup page with consistent layout
setup_page(
    title="Admin Dashboard",
    icon="👑",
    background_image="https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=2015&auto=format&fit=crop",
    page_class="admin-dashboard-page"
)

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