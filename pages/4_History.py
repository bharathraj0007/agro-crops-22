# ---- pages/4_History.py ----
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db_functions
import header

st.set_page_config(page_title="Recommendation History", page_icon="📜", layout="wide", initial_sidebar_state="collapsed")
def load_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), '..', file_name)
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style.css")
header.custom_header("History")

st.title("Recommendation History")

# --- UPDATED: Button arrangement ---
# Create a single column for the buttons to stack vertically, and a spacer column
button_col, _ = st.columns([0.2, 0.8])

with button_col:
    # Place both buttons in the same column
    st.markdown('<div class="stButton green">', unsafe_allow_html=True)
    if st.button("🔄 Refresh", use_container_width=True): 
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="stButton red">', unsafe_allow_html=True)
    if st.button("🗑️ Clear History", use_container_width=True): 
        db_functions.clear_history()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- History Table ---
try:
    history_df = db_functions.get_history()
    if not history_df.empty:
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No history records found.")
except Exception as e:
    st.error(f"Could not fetch history: {e}")