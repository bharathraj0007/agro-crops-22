"""Layout helper for consistent page structure across the app."""
import streamlit as st
import os

# Get root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_css(file_name="style_pro.css"):
    """Load CSS file consistently."""
    css_path = os.path.join(ROOT_DIR, file_name)
    try:
        with open(css_path, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found: {file_name}")

def apply_background(image_url, page_class="default-page"):
    """Apply consistent background styling to pages."""
    st.markdown(f'<div class="{page_class}">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <style>
    /* Main App Background */
    .stApp {{
        position: relative;
        background: #ecfdf5;
        background-attachment: fixed;
    }}
    
    /* Background Image Layer */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        background-image: url("{image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        opacity: 0.6;
        filter: brightness(1.1) saturate(1.05);
    }}
    
    /* Gradient Overlay */
    .stApp::after {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 1;
        background: rgba(236, 253, 245, 0.35);
        pointer-events: none;
    }}
    
    /* Content Layer */
    [data-testid="stAppViewContainer"] {{
        background: transparent;
        position: relative;
        z-index: 2;
    }}
    
    .main .block-container {{
        background: transparent;
        padding: 2rem 1rem;
        position: relative;
        z-index: 3;
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    /* Glass Effect Cards */
    div[data-testid="stVerticalBlock"] > div[style*="border"],
    div[data-testid="stExpander"],
    .stForm {{
        background: rgba(255, 255, 255, 0.98) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        border-radius: 1.25rem !important;
        border: none !important;
        box-shadow: 
            0 10px 40px rgba(0, 0, 0, 0.15),
            0 4px 16px rgba(16, 185, 129, 0.1) !important;
        transition: all 0.3s ease;
    }}
    
    /* Remove all borders */
    * {{
        border-color: transparent !important;
    }}
    
    div[data-testid="stVerticalBlock"] > div,
    div[data-testid="column"],
    div[data-testid="stHorizontalBlock"] {{
        border: none !important;
    }}
    
    /* Title Styling */
    .stApp h1 {{
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 2rem 2.5rem;
        border-radius: 1.5rem;
        border: none !important;
        border-left: 6px solid #10b981 !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        color: #111827 !important;
    }}
    
    /* Subheader Styling */
    .stApp h2, .stApp h3 {{
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 1.5rem 2rem;
        border-radius: 1.25rem;
        border: none !important;
        border-left: 6px solid #10b981 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
        color: #111827 !important;
        margin-bottom: 1.5rem;
    }}
    
    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.4) !important;
    }}
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {{
        background: rgba(255, 255, 255, 0.98) !important;
        border: none !important;
        border-radius: 0.75rem !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08) !important;
    }}
    
    /* Scrollbar */
    *::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    *::-webkit-scrollbar-track {{
        background: rgba(16, 185, 129, 0.05);
        border-radius: 10px;
    }}
    
    *::-webkit-scrollbar-thumb {{
        background: rgba(16, 185, 129, 0.3);
        border-radius: 10px;
    }}
    
    *::-webkit-scrollbar-thumb:hover {{
        background: rgba(16, 185, 129, 0.5);
    }}
    
    /* Prevent infinite scroll */
    body, html {{
        overflow-x: hidden !important;
        height: auto !important;
    }}
    
    [data-testid="stAppViewContainer"],
    .main {{
        min-height: 100vh !important;
        height: auto !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def close_page_div():
    """Close the page div."""
    st.markdown('</div>', unsafe_allow_html=True)

def setup_page(title, icon, layout="wide", css_file="style_pro.css", background_image=None, page_class="default-page"):
    """Setup page with consistent configuration."""
    # This should be called at the very start but after st.set_page_config
    load_css(css_file)
    
    if background_image:
        apply_background(background_image, page_class)
