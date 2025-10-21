# ---- pages/8_Admin_User_Management.py ----
import streamlit as st
import sys
import os
import pandas as pd

# --- Correctly set up the path to import shared files ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
import header
from sidebar import authenticated_sidebar
from layout_helper import setup_page, close_page_div

st.set_page_config(page_title="User Management", page_icon="👥", layout="wide", initial_sidebar_state="expanded")

# Setup page with consistent layout
setup_page(
    title="User Management",
    icon="👥",
    background_image="https://images.unsplash.com/photo-1521737604893-d14cc237f11d?q=80&w=2084&auto=format&fit=crop",
    page_class="admin-users-page",
    css_file="style.css"
)

# --- Authentication & Role Check ---
if not st.session_state.get('logged_in') or st.session_state.get('role') != 'Admin':
    st.error("You do not have permission to access this page.")
    st.page_link("app.py", label="Go back to Login")
    st.stop()

# Use the shared sidebar and header components for consistency
authenticated_sidebar()
header.custom_header("User Management")

st.title("User Management")
st.markdown("View, add, edit, or delete client profiles from this panel.")

# --- Tab Interface for User Management ---
tab1, tab2, tab3 = st.tabs(["View All Users", "Add New User", "Manage Existing Users"])

with tab1:
    st.subheader("All User Profiles")
    all_profiles = db_functions.get_all_profiles()
    if not all_profiles.empty:
        st.dataframe(all_profiles, use_container_width=True, hide_index=True)
    else:
        st.info("No user profiles found in the database.")

with tab2:
    st.subheader("Add a New User Profile")
    with st.form("add_user_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        farm_info = st.text_area("Farm Information")
        soil_type = st.selectbox("Soil Type", ["Loamy", "Sandy", "Clay", "Silty", "Peaty"])
        preferences = st.text_area("Farming Preferences")
        
        submitted = st.form_submit_button("Add User")
        if submitted:
            if name and email:
                db_functions.add_profile(name, email, farm_info, soil_type, preferences)
                st.success(f"Successfully added user: {name}")
                st.rerun()
            else:
                st.error("Full Name and Email are required fields.")

with tab3:
    st.subheader("Edit or Delete a User Profile")
    all_profiles_manage = db_functions.get_all_profiles() 
    if not all_profiles_manage.empty:
        profile_list = [f"{row['id']}: {row['name']}" for index, row in all_profiles_manage.iterrows()]
        selected_profile_str = st.selectbox("Select a profile to manage", profile_list)
        
        if selected_profile_str:
            profile_id = int(selected_profile_str.split(':')[0])
            selected_profile_data = all_profiles_manage[all_profiles_manage['id'] == profile_id].iloc[0]

            with st.form("edit_user_form"):
                st.write(f"**Managing Profile for: {selected_profile_data['name']}**")
                edit_name = st.text_input("Full Name", value=selected_profile_data['name'])
                edit_email = st.text_input("Email Address", value=selected_profile_data['email'])
                edit_farm_info = st.text_area("Farm Information", value=selected_profile_data['farm_info'])
                edit_soil_type = st.selectbox("Soil Type", ["Loamy", "Sandy", "Clay", "Silty", "Peaty"], index=["Loamy", "Sandy", "Clay", "Silty", "Peaty"].index(selected_profile_data['soil_type']))
                edit_preferences = st.text_area("Farming Preferences", value=selected_profile_data['preferences'])
                
                col_update, col_delete = st.columns(2)
                with col_update:
                    if st.form_submit_button("Update User"):
                        db_functions.update_profile(profile_id, edit_name, edit_email, edit_farm_info, edit_soil_type, edit_preferences)
                        st.success(f"Profile for {edit_name} updated successfully!")
                        st.rerun()
                with col_delete:
                    if st.form_submit_button("Delete User"):
                        db_functions.delete_profile(profile_id)
                        st.warning(f"Profile for {edit_name} has been deleted.")
                        st.rerun()
    else:
        st.info("No profiles to manage.")

