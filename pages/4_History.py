# ---- pages/4_History.py ----
import streamlit as st
import sys
import os
import pandas as pd

# Correctly set up the path to import shared files
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
from sidebar import authenticated_sidebar
from header import custom_header
from layout_helper import setup_page, close_page_div

st.set_page_config(page_title="Recommendation History", page_icon="📜", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if 'history_preferences' not in st.session_state:
    st.session_state.history_preferences = {}

# Setup page with consistent layout
setup_page(
    title="History",
    icon="📜",
    background_image="https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?q=80&w=2070&auto=format&fit=crop",
    page_class="history-page"
)

# Add beautiful background image to the History page
st.markdown(
    """
    <style>
    /* Main App Background for History Page */
    .stApp {
        position: relative;
        background: 
            linear-gradient(135deg, rgba(236, 253, 245, 0.90), rgba(220, 252, 231, 0.85)),
            #ecfdf5;
        background-attachment: fixed;
    }
    
    /* Background Image Layer */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        background-image: url("https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.60;
        filter: brightness(1.1) saturate(1.05);
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
        background: rgba(236, 253, 245, 0.35);
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
    
    /* Page Header Styling */
    .page-header h1 {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 2rem 2.5rem;
        border-radius: 1.5rem;
        border: none !important;
        border-left: 6px solid #10b981 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        color: #111827 !important;
        margin-bottom: 1rem;
    }
    
    .page-header p {
        background: rgba(255, 255, 255, 0.97) !important;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        color: #059669 !important;
        font-weight: 600;
    }
    
    /* Stats Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: none !important;
    }
    
    /* Headings */
    .stApp h3 {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #10b981 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        color: #111827 !important;
        margin-bottom: 1rem;
    }
    
    /* Action Buttons Container */
    .action-buttons {
        background: rgba(255, 255, 255, 0.97) !important;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(135deg, #059669, #047857) !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        font-weight: 600 !important;
    }
    
    /* Dataframe/Table */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        border: none !important;
    }
    
    /* Info Box */
    .stAlert {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 1rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
        border: none !important;
    }
    
    /* Remove all borders */
    div[data-testid="stVerticalBlock"] > div,
    div[class*="element-container"],
    section,
    section > div {
        border: none !important;
    }
    
    /* Custom Scrollbar */
    body::-webkit-scrollbar,
    html::-webkit-scrollbar,
    .main::-webkit-scrollbar,
    *::-webkit-scrollbar {
        width: 8px !important;
        height: 8px !important;
    }
    
    body::-webkit-scrollbar-track,
    html::-webkit-scrollbar-track,
    .main::-webkit-scrollbar-track,
    *::-webkit-scrollbar-track {
        background: rgba(16, 185, 129, 0.05) !important;
        border-radius: 10px !important;
    }
    
    body::-webkit-scrollbar-thumb,
    html::-webkit-scrollbar-thumb,
    .main::-webkit-scrollbar-thumb,
    *::-webkit-scrollbar-thumb {
        background: rgba(16, 185, 129, 0.3) !important;
        border-radius: 10px !important;
    }
    
    body::-webkit-scrollbar-thumb:hover,
    html::-webkit-scrollbar-thumb:hover,
    .main::-webkit-scrollbar-thumb:hover,
    *::-webkit-scrollbar-thumb:hover {
        background: rgba(16, 185, 129, 0.5) !important;
    }
    
    /* Firefox scrollbar */
    * {
        scrollbar-width: thin !important;
        scrollbar-color: rgba(16, 185, 129, 0.3) rgba(16, 185, 129, 0.05) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# # --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# # Use the shared sidebar and header components for consistency
# authenticated_sidebar()
# custom_header("History")

# Page header
st.markdown(
    """
    <div class="page-header">
        <h1>📜 Recommendation History</h1>
        <p>View and manage your crop recommendation history</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Statistics cards
try:
    history_df = db_functions.get_history()
    if not history_df.empty:
        # Stats row
        st.markdown("### 📊 Quick Stats")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("Total Recommendations", len(history_df))
        with stat_col2:
            unique_crops = history_df['crop'].nunique() if 'crop' in history_df.columns else 0
            st.metric("Unique Crops", unique_crops)
        with stat_col3:
            if 'timestamp' in history_df.columns:
                recent = pd.to_datetime(history_df['timestamp']).max().strftime('%Y-%m-%d')
                st.metric("Latest Entry", recent)
        with stat_col4:
            if 'crop' in history_df.columns:
                most_common = history_df['crop'].mode()[0] if not history_df['crop'].mode().empty else "N/A"
                st.metric("Most Recommended", most_common)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Action Buttons in a card
        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
        col1, col2, col3, _ = st.columns([1, 1.2, 1.2, 3])
        
        with col1:
            if st.button("🔄 Refresh", use_container_width=True): 
                st.rerun()
                
        with col2:
            if st.button("🗑️ Clear History", use_container_width=True, type="secondary"): 
                db_functions.clear_history()
                st.success("History cleared successfully!")
                st.rerun()
        
        # Download Button
        csv = history_df.to_csv(index=False).encode('utf-8')
        with col3:
            st.download_button(
               label="📥 Download CSV",
               data=csv,
               file_name='recommendation_history.csv',
               mime='text/csv',
               use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Display the table with header
        st.markdown("### 📋 Recommendation Records")
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No history records found. Start by getting crop recommendations!")
        if st.button("➡️ Go to Recommendations"):
            st.switch_page("pages/2_Recommendations.py")
except Exception as e:
    st.error(f"❌ Could not fetch history: {e}")

# Close page wrapper
st.markdown('</div>', unsafe_allow_html=True)

