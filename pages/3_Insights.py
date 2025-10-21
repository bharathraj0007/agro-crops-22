# ---- pages/3_Insights.py ----
import streamlit as st
import sys
import re
import numpy as np
import os
import pandas as pd

# Correctly set up the path to import shared files
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
import crop_data
from sidebar import authenticated_sidebar
from translations import get_text, get_language_switcher
from header import custom_header
from layout_helper import setup_page, close_page_div

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'
if 'insights_preferences' not in st.session_state:
    st.session_state.insights_preferences = {}
 
st.set_page_config(
    page_title=get_text("insights_title"),
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup page with consistent layout
setup_page(
    title="Insights",
    icon="📊",
    background_image="https://images.unsplash.com/photo-1574943320219-553eb213f72d?q=80&w=2070&auto=format&fit=crop",
    page_class="insights-page"
)
 
# Custom CSS for the Insights page
st.markdown("""
<style>
/* Background Image for Insights Page */
.stApp {
    position: relative;
    background: #f0fdf4 !important;
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
    background-image: url("https://images.unsplash.com/photo-1574943320219-553eb213f72d?q=80&w=2070&auto=format&fit=crop") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    background-repeat: no-repeat !important;
    opacity: 0.7 !important;
    filter: brightness(1.05) saturate(1.1);
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
    background: rgba(240, 253, 244, 0.4) !important;
    pointer-events: none;
}

/* Alternative targeting for Streamlit container */
[data-testid="stAppViewContainer"] {
    background: transparent !important;
    position: relative;
    z-index: 2;
}

/* Main content area styling */
.main .block-container {
    background: transparent !important;
    padding: 2rem 1rem;
    position: relative;
    z-index: 3;
}

/* Ensure app background takes precedence */
.stApp, .stApp > div {
    background: transparent !important;
}

.chart-card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
    transition: all 0.3s ease;
    height: 100%;
}
.chart-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(43, 147, 72, 0.15);
}
.chart-card h3 {
    color: #1b5e20;
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
</style>
""", unsafe_allow_html=True)
 
# # --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# authenticated_sidebar()
 
# custom_header("Insights")

# Page header
st.markdown(
    """
    <div class="page-header">
        <h1>📊 Agricultural Insights</h1>
        <p>Analyze trends and patterns from your recommendation history</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Helper function to calculate average yield
def parse_yield(yield_str):
    if isinstance(yield_str, str) and 'tons/ha' in yield_str:
        numbers = re.findall(r'\d+\.?\d*', yield_str)
        if numbers:
            return np.mean([float(num) for num in numbers])
    return 0

try:
    history_df = db_functions.get_history()
    if not history_df.empty:
        # Overview metrics at top in bordered container
        with st.container(border=True):
            st.markdown("### 📊 Overview Metrics")
            st.markdown("---")
            overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
            
            with overview_col1:
                st.metric("📝 Total Records", len(history_df))
            with overview_col2:
                unique_crops_count = history_df['crop'].nunique() if 'crop' in history_df.columns else 0
                st.metric("🌾 Unique Crops", unique_crops_count)
            with overview_col3:
                avg_temp = history_df['temperature'].mean() if 'temperature' in history_df.columns else 0
                st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f}°C")
            with overview_col4:
                avg_rainfall = history_df['rainfall'].mean() if 'rainfall' in history_df.columns else 0
                st.metric("💧 Avg Rainfall", f"{avg_rainfall:.1f}mm")
        
        st.markdown("<br>", unsafe_allow_html=True)
        yield_trend = None
        if len(history_df) > 1:
            yield_map = {k.lower(): v['yield'] for k, v in crop_data.CROP_DETAILS.items()}
            history_df['yield_str'] = history_df['crop'].str.lower().map(yield_map).fillna('0 tons/ha')
            history_df['avg_yield'] = history_df['yield_str'].apply(parse_yield)
            history_df['date'] = pd.to_datetime(history_df['timestamp']).dt.date
            yield_trend = history_df.groupby('date')['avg_yield'].mean().reset_index()

        # Average Soil Conditions
        with st.container(border=True):
            st.markdown("### 🧩 Soil Nutrient Analysis")
            st.markdown("---")
            avg_conditions = history_df[['nitrogen', 'phosphorus', 'potassium', 'ph']].mean()
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    "🧪 Nitrogen (N)",
                    f"{avg_conditions['nitrogen']:.1f}",
                    help="Average nitrogen content in kg/ha"
                )
            with col2:
                st.metric(
                    "🟠 Phosphorus (P)",
                    f"{avg_conditions['phosphorus']:.1f}",
                    help="Average phosphorus content in kg/ha"
                )
            with col3:
                st.metric(
                    "🟣 Potassium (K)",
                    f"{avg_conditions['potassium']:.1f}",
                    help="Average potassium content in kg/ha"
                )
            with col4:
                st.metric(
                    "⚗️ Soil pH",
                    f"{avg_conditions['ph']:.2f}",
                    help="Average pH level (7 is neutral)"
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Most Recommended Crops Chart - Full Width
        with st.container(border=True):
            st.markdown("### 🌾 Most Recommended Crops")
            st.markdown("---")
            crop_counts = db_functions.get_crop_counts()
            st.bar_chart(crop_counts.set_index('crop'), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Yield Trends Chart - Full Width
        with st.container(border=True):
            st.markdown("### 📈 Potential Yield Trends (tons/ha)")
            st.markdown("---")
            if yield_trend is not None:
                st.line_chart(yield_trend.set_index('date'), use_container_width=True)
            else:
                st.info("Need at least two recommendations to show a yield trend.")
    else:
        # Empty state with action
        st.markdown(
            """
            <div class="section-card" style="text-align: center; padding: 4rem 2rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📈</div>
                <h2>No Data Available Yet</h2>
                <p style="font-size: 1.1rem; color: var(--text-light); margin-bottom: 2rem;">
                    Start getting crop recommendations to see insights and analytics here.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🌾 Get Recommendations", use_container_width=False):
            st.switch_page("pages/2_Recommendations.py")
except Exception as e:
    st.error(f"❌ Could not load insights. Error: {e}")

# Footer spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Close page wrapper
close_page_div()
