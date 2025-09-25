# ---- app.py ----
import streamlit as st
import db_functions
import header

st.set_page_config(
    page_title="AgriAssist Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_css(file_name):
    with open(file_name) as f: 
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# --- ADD THIS WRAPPER to start the page-specific container ---
st.markdown('<div class="dashboard-background">', unsafe_allow_html=True)

header.custom_header("Dashboard")
db_functions.setup_database()

st.title("Welcome to the AgriAssist Dashboard")
st.markdown("Your central hub for smart crop recommendations and agricultural insights.")

try:
    stats = db_functions.get_dashboard_stats()
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Recommendations Made", value=stats['total'])
    col2.metric(label="Unique Crops Recommended", value=stats['unique_crops'])
    col3.metric(label="Last Recommendation", value=stats['latest'])
except Exception as e:
    st.warning(f"Could not load dashboard stats. Is the database running? Error: {e}")

st.markdown("---")

st.subheader("Explore Our Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="image-card">
            <img src="https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2070&auto=format&fit=crop">
            <h3>Smart Recommendations</h3>
            <p>Get AI-powered crop suggestions tailored to your farm's specific soil and climate conditions.</p>
        </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown("""
        <div class="image-card">
            <img src="https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?q=80&w=2070&auto=format&fit=crop">
            <h3>Data-Driven Insights</h3>
            <p>Analyze your recommendation history to discover trends and optimize your crop planning for future seasons.</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="image-card">
            <img src="https://images.unsplash.com/photo-1492496913980-501348b61469?q=80&w=1974&auto=format&fit=crop">
            <h3>Resource Management</h3>
            <p>Make informed decisions to better manage resources, reduce waste, and improve your farm's overall yield.</p>
        </div>
    """, unsafe_allow_html=True)

# --- ADD THIS WRAPPER to close the page-specific container ---
st.markdown('</div>', unsafe_allow_html=True)