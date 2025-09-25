# ---- pages/3_Insights.py ----
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db_functions
import header

st.set_page_config(page_title="Insights", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")
def load_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), '..', file_name)
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style.css")

# --- ADD THIS WRAPPER to start the page-specific container ---
st.markdown('<div class="insights-page">', unsafe_allow_html=True)

header.custom_header("Insights")

st.title("Agricultural Insights")
st.markdown("Analyze trends from your recommendation history.")

try:
    crop_counts = db_functions.get_crop_counts()
    if not crop_counts.empty:
        st.subheader("Most Frequently Recommended Crops")
        st.bar_chart(crop_counts.set_index('crop'))

        st.subheader("Average Soil Conditions")
        history_df = db_functions.get_history()
        avg_conditions = history_df[['nitrogen', 'phosphorus', 'potassium', 'ph']].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Avg. Nitrogen (N)", f"{avg_conditions['nitrogen']:.1f}")
        col2.metric("Avg. Phosphorus (P)", f"{avg_conditions['phosphorus']:.1f}")
        col3.metric("Avg. Potassium (K)", f"{avg_conditions['potassium']:.1f}")
        col4.metric("Avg. Soil pH", f"{avg_conditions['ph']:.1f}")
    else:
        st.info("No data available to generate insights. Please make some recommendations first.")
except Exception as e:
    st.error(f"Could not load insights. Error: {e}")

# --- ADD THIS WRAPPER to close the page-specific container ---
st.markdown('</div>', unsafe_allow_html=True)