import streamlit as st
import sys
import os

# --- Correctly set up the path to import shared files ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import header
from sidebar import authenticated_sidebar
from layout_helper import setup_page, close_page_div

st.set_page_config(page_title="Government Schemes", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

# Setup page with consistent layout
setup_page(
    title="Government Schemes",
    icon="🏦",
    background_image="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=2070&auto=format&fit=crop",
    page_class="govt-schemes-page"
)

# --- Authentication Check ---
# if not st.session_state.get('logged_in'):
#     st.error("You need to be logged in to access this page.")
#     st.page_link("app.py", label="Go to Login")
#     st.stop()

# Use the shared sidebar and header components for consistency
# authenticated_sidebar()
# header.custom_header("Govt. Schemes")

# Page header
st.markdown(
    """
    <div class="page-header">
        <h1>🏦 Government Schemes & Support</h1>
        <p>Explore agricultural schemes and financial assistance programs for farmers</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Disclaimer banner
st.markdown(
    """
    <div class="info-box">
        <p style="margin: 0; font-size: 0.95rem;">
            <strong>ℹ️ Disclaimer:</strong> Information provided here is for general guidance. 
            Always refer to official government portals for the latest details and application procedures.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Use tabs to separate Central and State schemes ---
central_tab, state_tab = st.tabs(["Central Government Schemes", "State Government Schemes (Karnataka)"])

with central_tab:
    st.markdown("### 🏛️ Major Central Government Initiatives")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("💵 Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)"):
        st.markdown("""
        - **Objective:** To provide direct income support to small and marginal farmers.
        - **Benefit:** Eligible farmers receive ₹6,000 per year in three equal installments.
        - **More Info:** Visit the [official PM-KISAN website](https://pmkisan.gov.in/).
        """)

    with st.expander("🛡️ Pradhan Mantri Fasal Bima Yojana (PMFBY)"):
        st.markdown("""
        - **Objective:** To provide insurance coverage and financial support to farmers in the event of failure of any of the notified crops as a result of natural calamities, pests & diseases.
        - **Benefit:** Stabilizes the income of farmers to ensure their continuance in farming.
        - **More Info:** Visit the [official PMFBY website](https://pmfby.gov.in/).
        """)

    with st.expander("💳 Kisan Credit Card (KCC) Scheme"):
        st.markdown("""
        - **Objective:** To meet the comprehensive credit requirements of the agriculture sector by giving financial support to farmers.
        - **Benefit:** Provides term loans and access to credit at concessional rates of interest.
        - **More Info:** Contact your nearest nationalized bank.
        """)
        
    with st.expander("🧩 Soil Health Card Scheme"):
        st.markdown("""
        - **Objective:** To help farmers to improve productivity from their farms by providing them information on the nutrient status of their soil.
        - **Benefit:** Farmers receive a soil health card which provides crop-wise recommendations of nutrients and fertilizers required for the individual farms.
        - **More Info:** Visit the [official Soil Health Card portal](https://soilhealth.dac.gov.in/).
        """)

with state_tab:
    st.markdown("### 🏙️ Key Schemes by the Government of Karnataka")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("🌾 Raitha Siri Yojane (Millet Promotion)"):
        st.markdown("""
        - **Objective:** To encourage farmers to grow millets, which are nutritious and drought-resistant.
        - **Benefit:** Financial assistance of ₹10,000 per hectare for farmers cultivating minor millets.
        - **More Info:** Visit the [Karnataka State Agriculture Department website](https://raitamitra.karnataka.gov.in/).
        """)

    with st.expander("💧 Krishi Bhagya (Farm Ponds)"):
        st.markdown("""
        - **Objective:** To promote sustainable agriculture in rain-fed areas through efficient management of rainwater.
        - **Benefit:** Subsidies for constructing farm ponds ('Krishi Honda') for rainwater harvesting and protective irrigation.
        - **More Info:** Contact your local Raitha Samparka Kendra.
        """)

    with st.expander("📱 Bhoomi Project (Digital Land Records)"):
        st.markdown("""
        - **Objective:** To digitize and manage land records for transparency and easy access.
        - **Benefit:** Farmers can get their RTC (Record of Rights, Tenancy and Crops) online, which is essential for availing loans and other benefits.
        - **More Info:** Visit the [official Bhoomi portal](https://landrecords.karnataka.gov.in/service2/).
        """)

# Additional resources section
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🔗 Useful Resources")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="section-card" style="text-align: center;">
            <h4>🌐 Official Portals</h4>
            <p style="font-size: 0.9rem;">Ministry of Agriculture & Farmers Welfare</p>
            <p style="font-size: 0.9rem;">PM-KISAN Portal</p>
            <p style="font-size: 0.9rem;">PMFBY Portal</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        """
        <div class="section-card" style="text-align: center;">
            <h4>📞 Helpline Numbers</h4>
            <p style="font-size: 0.9rem;">PM-KISAN: 011-24300606</p>
            <p style="font-size: 0.9rem;">Kisan Call Centre: 1800-180-1551</p>
            <p style="font-size: 0.9rem;">PMFBY: 1800-180-1551</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <div class="section-card" style="text-align: center;">
            <h4>📧 Contact Support</h4>
            <p style="font-size: 0.9rem;">For scheme-related queries</p>
            <p style="font-size: 0.9rem;">Visit your nearest Krishi Vigyan Kendra</p>
            <p style="font-size: 0.9rem;">Or Agricultural Extension Office</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Close page wrapper
st.markdown('</div>', unsafe_allow_html=True)
