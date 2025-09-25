# ---- pages/5_Support.py ----
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import header

st.set_page_config(page_title="Support", page_icon="💬", layout="wide", initial_sidebar_state="collapsed")
def load_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), '..', file_name)
    with open(css_path) as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style.css")

# --- ADD THIS WRAPPER to start the page-specific container ---
st.markdown('<div class="support-page">', unsafe_allow_html=True)

header.custom_header("Support")

st.title("Support & FAQ")

st.subheader("Frequently Asked Questions")
with st.expander("How does the crop recommendation work?"):
    st.write("Our system uses a machine learning model to analyze your input parameters and predict the most suitable crops.")
with st.expander("Is my data stored securely?"):
    st.write("Yes, your recommendation history is stored in a private database and is only used to provide insights.")
with st.expander("How can I improve recommendation accuracy?"):
    st.write("For best results, use data from a professional soil test for the N, P, K, and pH values.")

st.markdown("---")
st.subheader("Contact Us")
with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    if st.form_submit_button("Submit"):
        st.success("Thank you for your message! We will get back to you shortly.")

# --- ADD THIS WRAPPER to close the page-specific container ---
st.markdown('</div>', unsafe_allow_html=True)