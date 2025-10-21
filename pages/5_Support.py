# ---- pages/5_Support.py ----
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

st.set_page_config(page_title="Support", page_icon="💬", layout="wide", initial_sidebar_state="expanded")

def load_css(file_name):
    # Correct path to find CSS from the pages subfolder
    css_path = os.path.join(ROOT_DIR, file_name)
    with open(css_path, encoding='utf-8') as f: 
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style_pro.css")

# Add page-specific CSS class
st.markdown('<div class="support-page">', unsafe_allow_html=True)

# Add beautiful background image for Support page
st.markdown(
    """
    <style>
    /* Main App Background for Support Page - Farmer/Help Theme */
    .stApp {
        position: relative;
        background: 
            linear-gradient(135deg, rgba(254, 243, 199, 0.90), rgba(253, 230, 138, 0.85)),
            #fef3c7;
        background-attachment: fixed;
    }
    
    /* Background Image Layer - Farmer/Support Theme */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        background-image: url("https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.55;
        filter: brightness(1.15) saturate(1.1);
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
        background: rgba(254, 243, 199, 0.30);
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
    
    /* Page Header */
    .page-header h1 {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 2rem 2.5rem;
        border-radius: 1.5rem;
        border: none !important;
        border-left: 6px solid #f59e0b !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        color: #111827 !important;
        margin-bottom: 1rem;
    }
    
    .page-header p {
        background: rgba(255, 255, 255, 0.97) !important;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        color: #d97706 !important;
        font-weight: 600;
    }
    
    /* Headings */
    .stApp h2, .stApp h3 {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1rem 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #f59e0b !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        color: #111827 !important;
        margin-bottom: 1rem;
    }
    
    /* Cards and Containers */
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="stExpander"],
    .stForm {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 1.25rem !important;
        border: none !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
        padding: 1.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3) !important;
        transition: transform 0.2s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(245, 158, 11, 0.4) !important;
        background: linear-gradient(135deg, #d97706, #b45309) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.98) !important;
        border: none !important;
        border-radius: 0.75rem !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Remove all borders */
    div[data-testid="stVerticalBlock"] > div,
    section, section > div {
        border: none !important;
    }
    
    /* Custom Scrollbar */
    *::-webkit-scrollbar { width: 8px !important; }
    *::-webkit-scrollbar-track { background: rgba(245, 158, 11, 0.05) !important; border-radius: 10px !important; }
    *::-webkit-scrollbar-thumb { background: rgba(245, 158, 11, 0.3) !important; border-radius: 10px !important; }
    *::-webkit-scrollbar-thumb:hover { background: rgba(245, 158, 11, 0.5) !important; }
    * { scrollbar-width: thin !important; scrollbar-color: rgba(245, 158, 11, 0.3) rgba(245, 158, 11, 0.05) !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# Initialize session state for contact form fields
if 'contact_name' not in st.session_state:
    st.session_state.contact_name = ""
if 'contact_email' not in st.session_state:
    st.session_state.contact_email = ""
if 'contact_subject' not in st.session_state:
    st.session_state.contact_subject = "General Inquiry"
if 'contact_message' not in st.session_state:
    st.session_state.contact_message = ""

# # Use the shared sidebar and header components for consistency
# authenticated_sidebar()
# header.custom_header("Support")

# Page header
st.markdown(
    """
    <div class="page-header">
        <h1>💬 Support & Help Center</h1>
        <p>Find answers to common questions or contact our support team</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Quick help cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="section-card" style="text-align: center;">
            <h3>📚 Documentation</h3>
            <p>Learn how to use AgriAssist effectively</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <div class="section-card" style="text-align: center;">
            <h3>🎥 Video Tutorials</h3>
            <p>Watch step-by-step guides</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <div class="section-card" style="text-align: center;">
            <h3>💡 Tips & Tricks</h3>
            <p>Get the most out of the platform</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# FAQ Section
st.markdown("### ❓ Frequently Asked Questions")

with st.expander("🌾 How does the crop recommendation work?"):
    st.markdown("""
    Our **AI-powered system** analyzes multiple factors:
    - 🧪 Soil nutrients (N, P, K levels)
    - 🌡️ Temperature and humidity
    - 💧 Rainfall patterns
    - 📍 Geographic location
    - ⚗️ Soil pH levels
    
    The machine learning model compares your data with thousands of successful crop cultivation records 
    to recommend the top 3 most suitable crops for your conditions.
    """)

with st.expander("🔒 Is my data stored securely?"):
    st.markdown("""
    **Yes, your data is completely secure!**
    
    - ✅ All data is stored locally on your machine
    - ✅ No data is sent to external servers
    - ✅ Your recommendation history is private
    - ✅ Only used to provide personalized insights
    
    We take your privacy seriously and comply with data protection standards.
    """)

with st.expander("📈 How can I improve recommendation accuracy?"):
    st.markdown("""
    For **best results**, follow these tips:
    
    1. 🔬 **Get Professional Soil Testing**: Use lab-tested values for N, P, K, and pH
    2. 📍 **Accurate Location**: Select your exact farm location on the map
    3. 🌦️ **Current Weather**: Allow live weather data integration
    4. 📊 **Regular Updates**: Update soil parameters seasonally
    5. 📝 **Track Results**: Use the History feature to track what works
    
    *Professional soil testing can be done at local agricultural extension offices.*
    """)

with st.expander("🗺️ How do I use the location map?"):
    st.markdown("""
    **Two ways to select your location:**
    
    1. 🔍 **Search**: Type your farm's address or nearest city
    2. 🖱️ **Click**: Click directly on the map to drop a pin
    
    The system will automatically fetch weather data for your selected location.
    """)

with st.expander("💾 Can I export my recommendation history?"):
    st.markdown("""
    **Yes!** Go to the **History** page and click the **"📥 Download CSV"** button.
    
    You can:
    - Open it in Excel or Google Sheets
    - Analyze trends over time
    - Share with agricultural consultants
    - Keep records for future reference
    """)

with st.expander("🌐 Does this work offline?"):
    st.markdown("""
    **Partially:**
    
    - ✅ Core recommendation engine works offline
    - ✅ Database and history tracking works offline
    - ❌ Live weather data requires internet
    - ❌ Map features require internet
    
    You can use manual weather inputs when offline.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# Contact Form
st.markdown("### 📧 Contact Our Support Team")
st.markdown("Can't find what you're looking for? Send us a message and we'll get back to you!")

col1, col2 = st.columns([2, 1])
with col1:
    with st.form("contact_form"):
        name = st.text_input("Your Name *", placeholder="Enter your full name", 
                            value=st.session_state.contact_name, key="contact_name_input")
        email = st.text_input("Your Email *", placeholder="your.email@example.com", 
                             value=st.session_state.contact_email, key="contact_email_input")
        subject = st.selectbox(
            "Subject *",
            ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Other"],
            index=["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Other"].index(st.session_state.contact_subject) if st.session_state.contact_subject in ["General Inquiry", "Technical Support", "Feature Request", "Bug Report", "Other"] else 0,
            key="contact_subject_input"
        )
        message = st.text_area(
            "Your Message *", 
            placeholder="Describe your question or issue in detail...",
            height=150,
            value=st.session_state.contact_message,
            key="contact_message_input"
        )
        
        submitted = st.form_submit_button("📤 Send Message", use_container_width=True)
        
        if submitted:
            # Update session state with form values
            st.session_state.contact_name = name
            st.session_state.contact_email = email
            st.session_state.contact_subject = subject
            st.session_state.contact_message = message
            
            if name and email and message:
                db_functions.save_contact_message(name, email, message)
                st.success("✅ Thank you! Your message has been sent. We'll respond within 24 hours.")
                # Clear the form fields after successful submission
                st.session_state.contact_name = ""
                st.session_state.contact_email = ""
                st.session_state.contact_subject = "General Inquiry"
                st.session_state.contact_message = ""
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields.")

with col2:
    st.markdown(
        """
        <div class="contact-section">
            <h4>📞 Other Ways to Reach Us</h4>
            <br>
            <p><strong>📧 Email:</strong><br>support@agriassist.com</p>
            <p><strong>📱 Phone:</strong><br>+91 1800-XXX-XXXX</p>
            <p><strong>⏰ Hours:</strong><br>Mon-Fri: 9AM - 6PM IST</p>
            <p><strong>🌐 Community:</strong><br>Join our farmer forums</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Close page wrapper
st.markdown('</div>', unsafe_allow_html=True)

