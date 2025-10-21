import streamlit as st
import sys
import os

# --- Correctly set up the path to import shared files ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
import header

st.set_page_config(page_title="Why AgriAssist?", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

def load_css(file_name):
    # Correct path to find CSS from the pages subfolder
    css_path = os.path.join(ROOT_DIR, file_name)
    with open(css_path, encoding='utf-8') as f: 
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style_pro.css")

# --- Authentication Check ---
# For a marketing page, you might want to show this even to non-logged-in users.
# For now, we'll keep the authentication check for consistency.
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# header.custom_header("Marketing")

# --- Add a wrapper for page-specific styles ---
st.markdown('<div class="marketing-page">', unsafe_allow_html=True)

# --- 1. Hero Banner ---
st.markdown(
    """
    <div class="hero-banner">
        <h1>Farm Smarter, Not Harder</h1>
        <p>Let AI guide your planting decisions. AgriAssist analyzes your unique farm conditions to recommend the most profitable and suitable crops, season after season.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- 2. Features Section ---
st.markdown("## Key Features of AgriAssist")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔬</div>
            <h3>Hyper-Personalized Analysis</h3>
            <p>Our AI considers your specific soil nutrients (N, P, K), pH levels, and local weather patterns to provide recommendations tailored to your land.</p>
        </div>
        """, unsafe_allow_html=True)
with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🌦️</div>
            <h3>Live Weather Integration</h3>
            <p>Get recommendations based on real-time and historical weather data for your exact location, ensuring climate suitability for your chosen crops.</p>
        </div>
        """, unsafe_allow_html=True)
with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Productivity-Focused</h3>
            <p>Our model doesn't just find a match—it recommends crops with high yield potential and market value, helping you maximize your farm's profitability.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- 3. How It Works Section ---
st.markdown("## How It Works: A Simple 3-Step Process")
st.image("https://images.unsplash.com/photo-1586796676769-ce69b232e0a6?q=80&w=2070&auto=format&fit=crop", caption="From Data to Decision")
st.markdown(
    """
    <div class="how-it-works">
        <div class="step">
            <div class="step-number">1</div>
            <div class="step-text">
                <h4>Input Your Data</h4>
                <p>Select your farm's location on the interactive map and input your soil's nutrient and pH values.</p>
            </div>
        </div>
        <div class="step">
            <div class="step-number">2</div>
            <div class="step-text">
                <h4>AI Analysis</h4>
                <p>Our powerful algorithm instantly analyzes your data against thousands of agricultural data points to find the best crop matches.</p>
            </div>
        </div>
        <div class="step">
            <div class="step-number">3</div>
            <div class="step-text">
                <h4>Get Recommendations</h4>
                <p>Receive a list of the top 3 recommended crops, complete with confidence scores, yield potential, and water needs.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 4. Benefits Section ---
st.markdown("## Benefits for Your Farm")
col1, col2 = st.columns(2)
with col1:
    st.image("https://images.unsplash.com/photo-1620205492110-a2908a8a3a04?q=80&w=1964&auto=format&fit=crop", use_column_width=True)
with col2:
    st.markdown(
        """
        <div class="benefits-list">
            <ul>
                <li>✅ <strong>Increase Profitability:</strong> Choose crops with higher yield and market demand.</li>
                <li>💧 <strong>Optimize Resources:</strong> Reduce waste by selecting crops that are naturally suited to your environment.</li>
                <li>🌿 <strong>Promote Sustainability:</strong> Improve soil health and reduce the need for excessive fertilizers or irrigation.</li>
                <li>🧠 <strong>Make Confident Decisions:</strong> Take the guesswork out of farming with data-backed insights.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --- 5. Call-to-Action ---
st.markdown(
    """
    <div class="cta-section">
        <h2>Ready to Transform Your Farm?</h2>
        <p>Start making smarter, data-driven decisions today. Get your first crop recommendation in just a few clicks.</p>
    </div>
    """, unsafe_allow_html=True)

if st.button("Go to Recommendations Page"):
    st.switch_page("pages/2_Recommendations.py")

st.markdown('</div>', unsafe_allow_html=True) # Closes the marketing-page wrapper

