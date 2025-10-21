# ---- pages/9_Admin_Crop_Management.py ----
import streamlit as st
import sys
import os
import pandas as pd

# --- Correctly set up the path to import shared files ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
import header
import crop_data
from sidebar import authenticated_sidebar
from layout_helper import setup_page, close_page_div

st.set_page_config(page_title="Crop Management", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

# Setup page with consistent layout
setup_page(
    title="Crop Management",
    icon="🌿",
    background_image="https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=2070&auto=format&fit=crop",
    page_class="admin-crops-page",
    css_file="style.css"
)

# --- Authentication & Role Check ---
if not st.session_state.get('logged_in') or st.session_state.get('role') != 'Admin':
    st.error("You do not have permission to access this page.")
    st.page_link("app.py", label="Go back to Login")
    st.stop()

# Use the shared sidebar and header components for consistency
authenticated_sidebar()
header.custom_header("Crop Management")

# --- One-time data population from crop_data.py ---
# This will run once to move your static data into the new database table
db_functions.populate_crops_table_if_empty()

st.title("Crop Management")
st.markdown("View, add, edit, and delete crop data used in the application.")

# --- Tab Interface for Crop Management ---
tab1, tab2, tab3 = st.tabs(["View All Crops", "Add New Crop", "Manage Existing Crops"])

with tab1:
    st.subheader("All Crops in Database")
    all_crops = db_functions.get_all_crops()
    if not all_crops.empty:
        st.dataframe(all_crops, use_container_width=True, hide_index=True)
    else:
        st.warning("No crop data found. The initial population may have failed.")

with tab2:
    st.subheader("Add a New Crop")
    with st.form("add_crop_form"):
        name = st.text_input("Crop Name (e.g., Wheat)")
        description = st.text_area("Description")
        water = st.selectbox("Water Consumption", ["Low", "Moderate", "High", "Very High"])
        crop_yield = st.text_input("Yield (e.g., 4-5 tons/ha)")
        image_path = st.text_input("Image Path (e.g., images/wheat.jpg)")
        
        submitted = st.form_submit_button("Add Crop")
        if submitted:
            if name and description and image_path:
                try:
                    db_functions.add_crop(name, description, water, crop_yield, image_path)
                    st.success(f"Successfully added crop: {name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to add crop. It might already exist. Error: {e}")
            else:
                st.error("Crop Name, Description, and Image Path are required fields.")

with tab3:
    st.subheader("Edit or Delete a Crop")
    all_crops_manage = db_functions.get_all_crops()
    if not all_crops_manage.empty:
        # Create a list of 'ID: Name' for the selectbox
        crop_list = [f"{row['id']}: {row['name']}" for index, row in all_crops_manage.iterrows()]
        selected_crop_str = st.selectbox("Select a crop to manage", crop_list)
        
        if selected_crop_str:
            crop_id = int(selected_crop_str.split(':')[0])
            selected_crop_data = all_crops_manage[all_crops_manage['id'] == crop_id].iloc[0]

            with st.form("edit_crop_form"):
                st.write(f"**Managing Crop: {selected_crop_data['name']}**")
                
                edit_name = st.text_input("Crop Name", value=selected_crop_data['name'])
                edit_description = st.text_area("Description", value=selected_crop_data['description'])
                water_options = ["Low", "Moderate", "High", "Very High"]
                edit_water = st.selectbox("Water Consumption", water_options, index=water_options.index(selected_crop_data['water_consumption']))
                edit_yield = st.text_input("Yield", value=selected_crop_data['yield'])
                edit_image_path = st.text_input("Image Path", value=selected_crop_data['image_path'])
                
                col_update, col_delete = st.columns(2)
                with col_update:
                    if st.form_submit_button("Update Crop"):
                        db_functions.update_crop(crop_id, edit_name, edit_description, edit_water, edit_yield, edit_image_path)
                        st.success(f"Crop '{edit_name}' updated successfully!")
                        st.rerun()
                with col_delete:
                    st.markdown('<div class="stButton red">', unsafe_allow_html=True)
                    if st.form_submit_button("Delete Crop"):
                        db_functions.delete_crop(crop_id)
                        st.warning(f"Crop '{edit_name}' has been deleted.")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No crops to manage.")

