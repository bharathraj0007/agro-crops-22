# ---- pages/5_Support.py ----
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

st.set_page_config(page_title="Support", page_icon="💬", layout="wide", initial_sidebar_state="expanded")

# Setup page with consistent layout
setup_page(
    title="Support",
    icon="💬",
    background_image="https://images.unsplash.com/photo-1553484771-047a44eee27a?q=80&w=2070&auto=format&fit=crop",
    page_class="support-page"
)

# Page-specific styling enhancements
st.markdown(
    """
    <style>
    /* Support page specific styling */
    .support-page .page-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .support-page .page-header h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .support-page .page-header p {
        font-size: 1.2rem;
        color: #6b7280;
    }
    
    /* Quick help cards */
    .section-card {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 2rem 1.5rem;
        border-radius: 1.25rem;
        border: none !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(16, 185, 129, 0.2) !important;
    }
    
    .section-card h3 {
        background: none !important;
        padding: 0 !important;
        margin: 1rem 0 0.5rem 0 !important;
        box-shadow: none !important;
        border: none !important;
        font-size: 1.5rem;
        color: #10b981 !important;
    }
    
    .section-card p {
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        color: #6b7280;
        margin: 0;
    }
    
    /* Contact info section */
    .contact-section {
        background: rgba(255, 255, 255, 0.98);
        padding: 2rem;
        border-radius: 1.25rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    
    .contact-section h4 {
        color: #10b981;
        margin-bottom: 1rem;
        font-size: 1.3rem;
    }
    
    .contact-section p {
        background: none !important;
        padding: 0.5rem 0 !important;
        box-shadow: none !important;
        color: #374151;
        margin: 0.75rem 0;
        font-size: 0.95rem;
    }
    
    .contact-section strong {
        color: #10b981;
        font-weight: 600;
    }
    
    /* FAQ Expanders */
    div[data-testid="stExpander"] {
        margin-bottom: 1rem;
    }
    
    div[data-testid="stExpander"] summary {
        font-size: 1.1rem;
        font-weight: 600;
        color: #111827;
        padding: 1rem;
    }
    
    div[data-testid="stExpander"] summary:hover {
        color: #10b981;
    }
    
    /* Form styling */
    .stForm {
        padding: 2rem !important;
    }
    
    /* Consistent column alignment */
    div[data-testid="column"] {
        padding: 0.5rem;
    }
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
st.title("💬 Support & Help Center")
st.markdown(
    "<p style='text-align: center; font-size: 1.2rem; color: #6b7280; margin-bottom: 2rem;'>Find answers to common questions or contact our support team</p>",
    unsafe_allow_html=True
)

# Quick help cards
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 3rem;">📚</div>
                <h3 style="margin: 1rem 0 0.5rem 0; background: none !important; padding: 0 !important; box-shadow: none !important; border: none !important;">Documentation</h3>
                <p style="background: none !important; padding: 0 !important; box-shadow: none !important; color: #6b7280;">Learn how to use AgriAssist effectively</p>
            </div>
            """,
            unsafe_allow_html=True
        )
with col2:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 3rem;">🎥</div>
                <h3 style="margin: 1rem 0 0.5rem 0; background: none !important; padding: 0 !important; box-shadow: none !important; border: none !important;">Video Tutorials</h3>
                <p style="background: none !important; padding: 0 !important; box-shadow: none !important; color: #6b7280;">Watch step-by-step guides</p>
            </div>
            """,
            unsafe_allow_html=True
        )
with col3:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 3rem;">💡</div>
                <h3 style="margin: 1rem 0 0.5rem 0; background: none !important; padding: 0 !important; box-shadow: none !important; border: none !important;">Tips & Tricks</h3>
                <p style="background: none !important; padding: 0 !important; box-shadow: none !important; color: #6b7280;">Get the most out of the platform</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# FAQ Section
with st.container(border=True):
    st.markdown("## ❓ Frequently Asked Questions")
    st.markdown("---")
    
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
st.markdown("## 📧 Contact Our Support Team")
st.markdown("<p style='font-size: 1.1rem; color: #6b7280; margin-bottom: 1.5rem;'>Can't find what you're looking for? Send us a message and we'll get back to you!</p>", unsafe_allow_html=True)

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
    with st.container(border=True):
        st.markdown("#### 📞 Other Ways to Reach Us")
        st.markdown("---")
        st.markdown("""
        **📧 Email:**  
        support@agriassist.com
        
        **📱 Phone:**  
        +91 1800-XXX-XXXX
        
        **⏰ Hours:**  
        Mon-Fri: 9AM - 6PM IST
        
        **🌐 Community:**  
        Join our farmer forums
        """)

# Footer spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Close page wrapper
close_page_div()

