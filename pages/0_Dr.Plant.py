# ---- pages/0_Dr.Plant.py ----
import streamlit as st
import sys
import os

# --- Path setup ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

import db_functions
from layout_helper import setup_page, close_page_div

# Initialize page config
st.set_page_config(
    page_title="Dr. Plant - AgriAssist",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup page with consistent layout
setup_page(
    title="Dr. Plant",
    icon="🌿",
    background_image="https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?q=80&w=2070&auto=format&fit=crop",
    page_class="drplant-page"
)

# Initialize session state
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

# Disease database (in a real app, this would come from a database)
DISEASE_DB = {
    'Tomato': {
        'Early Blight': {
            'symptoms': 'Dark spots with concentric rings on leaves, yellowing leaves, defoliation',
            'causes': 'Fungus (Alternaria solani)',
            'treatment': 'Apply copper-based fungicides, remove infected leaves, ensure good air circulation',
            'prevention': 'Rotate crops, use disease-free seeds, avoid overhead watering',
            'severity': 'Moderate to High'
        },
        'Late Blight': {
            'symptoms': 'Water-soaked spots on leaves, white fungal growth, rapid plant death',
            'causes': 'Oomycete (Phytophthora infestans)',
            'treatment': 'Apply fungicides containing chlorothalonil or mancozeb, remove and destroy infected plants',
            'prevention': 'Plant resistant varieties, ensure good drainage, avoid working with wet plants',
            'severity': 'High'
        },
        'Bacterial Spot': {
            'symptoms': 'Small, dark, water-soaked spots on leaves and fruits',
            'causes': 'Bacteria (Xanthomonas spp.)',
            'treatment': 'Copper-based bactericides, remove infected plants',
            'prevention': 'Use disease-free seeds, avoid overhead watering, practice crop rotation',
            'severity': 'Moderate'
        }
    },
    'Rice': {
        'Blast': {
            'symptoms': 'Diamond-shaped lesions on leaves, collar rot on seedlings',
            'causes': 'Fungus (Magnaporthe oryzae)',
            'treatment': 'Apply fungicides like tricyclazole or azoxystrobin',
            'prevention': 'Plant resistant varieties, maintain proper water management',
            'severity': 'High'
        },
        'Bacterial Leaf Blight': {
            'symptoms': 'Yellowish water-soaked streaks on leaf margins',
            'causes': 'Bacteria (Xanthomonas oryzae)',
            'treatment': 'Streptomycin or copper-based bactericides',
            'prevention': 'Use resistant varieties, avoid excessive nitrogen',
            'severity': 'Moderate to High'
        }
    },
    'Wheat': {
        'Rust': {
            'symptoms': 'Orange-brown pustules on leaves and stems',
            'causes': 'Fungus (Puccinia spp.)',
            'treatment': 'Fungicides like propiconazole or tebuconazole',
            'prevention': 'Plant resistant varieties, avoid excessive nitrogen',
            'severity': 'High'
        },
        'Powdery Mildew': {
            'symptoms': 'White powdery growth on leaves',
            'causes': 'Fungus (Blumeria graminis)',
            'treatment': 'Sulfur or potassium bicarbonate sprays',
            'prevention': 'Ensure good air circulation, avoid dense planting',
            'severity': 'Moderate'
        }
    }
}

# Add a visually appealing background image to the page
st.markdown(
    """
    <style>
    body {
        background-image: linear-gradient(rgba(40,60,20,0.25), rgba(40,60,20,0.25)), url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1500&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }
    .stApp {
        background: rgba(255,255,255,0.70);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page header
st.markdown("""
    <h1 class="gradient-title">🌿 Dr. Plant</h1>
    <div class="custom-divider"></div>
    <div class="card" style="margin-top:1.2rem; padding:2.5rem 2rem;">
        <h3>Your AI-Powered Plant Doctor</h3>
        <p>Identify plant diseases, get treatment recommendations, and learn preventive measures to keep your crops healthy.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🔍 Identify Plant Disease")

# Plant selection
st.markdown('<div class="form-group"><label class="form-label">Select Plant Type</label>', unsafe_allow_html=True)
plant_type = st.selectbox(
    "",
    ["Tomato", "Rice", "Wheat", "Potato", "Cotton"],
    index=0,
    help="Select the type of plant you need help with"
)
st.markdown(f"**Selected Plant:** {plant_type}</div>", unsafe_allow_html=True)

# Symptom selection
symptoms = st.multiselect(
    "Observed Symptoms",
    ["Yellowing leaves", "Spots on leaves", "Wilting", "Mold/Fungus", "Stunted growth", "Leaf curling"],
    help="Select all symptoms you've observed"
)

# Image upload
uploaded_file = st.file_uploader("Upload a photo of the affected plant (optional)", type=["jpg", "jpeg", "png"])

if st.button("🔍 Analyze Plant"):
    if not symptoms and not uploaded_file:
        st.warning("Please provide symptoms or upload a photo for analysis")
    else:
        st.session_state.analyzing = True
        st.rerun()

if st.session_state.analyzing:
    st.markdown(f"### 🔬 Analysis Results for {plant_type}")
    # In a real app, this would use a machine learning model for prediction
    if plant_type in DISEASE_DB:
        diseases = DISEASE_DB[plant_type]
        report_lines = [f"Analysis Report for {plant_type}\n"]
        for disease, info in diseases.items():
            with st.expander(f"🦠 {disease}", expanded=True):
                st.markdown(f"""
                <div class="card">
                    <p><strong>🔍 Symptoms:</strong> {info['symptoms']}</p>
                    <p><strong>📌 Causes:</strong> {info['causes']}</p>
                    <p><strong>💊 Treatment:</strong> {info['treatment']}</p>
                    <p><strong>🛡️ Prevention:</strong> {info['prevention']}</p>
                    <p><strong>⚠ Severity:</strong> {info['severity']}</p>
                </div>
                """, unsafe_allow_html=True)
                report_lines.append(f"Disease: {disease}\n  Symptoms: {info['symptoms']}\n  Causes: {info['causes']}\n  Treatment: {info['treatment']}\n  Prevention: {info['prevention']}\n  Severity: {info['severity']}\n")
        report_content = "\n".join(report_lines)
        st.download_button(
            label="Download Report",
            data=report_content,
            file_name=f"{plant_type}_analysis_report.txt",
            mime="text/plain"
        )
    else:
        st.info("No specific disease information available for this plant. Here are some general tips:")
        st.markdown("""
        <div class="card">
            <h4>General Plant Care Tips</h4>
            <ul>
                <li>Ensure proper watering - not too much, not too little</li>
                <li>Check for proper sunlight exposure</li>
                <li>Look for pests on the underside of leaves</li>
                <li>Ensure good soil drainage</li>
                <li>Consider soil testing for nutrient deficiencies</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    if st.button("🔄 Analyze Another Plant"):
        st.session_state.analyzing = False
        st.rerun()
else:
    st.markdown("### 📋 How It Works")
    st.markdown("""
    <div class="card" style="padding:2.5rem 2rem;">
        <ol>
            <li>Select the type of plant you need help with</li>
            <li>Select the symptoms you've observed</li>
            <li>Optionally, upload a photo of the affected plant</li>
            <li>Click 'Analyze Plant' to get diagnosis and treatment options</li>
        </ol>
        <p><em>Note: For best results, provide clear photos of both the affected area and the entire plant.</em></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🌱 Common Plant Problems")
    st.markdown("""
    <div class="plant-grid" style="margin-left:2.5vw; margin-right:2.5vw;">
                <div class="plant-card">
                    <h4>🌡️ Environmental Stress</h4>
                    <p>Extreme temperatures, improper watering, or poor soil conditions can cause various symptoms.</p>
                </div>
                <div class="plant-card">
                    <h4>🐛 Pest Infestation</h4>
                    <p>Insects and other pests can cause visible damage to leaves, stems, and fruits.</p>
                </div>
                <div class="plant-card">
                    <h4>🦠 Diseases</h4>
                    <p>Fungal, bacterial, or viral infections that can spread quickly if not treated.</p>
                </div>
                <div class="plant-card">
                    <h4>🌿 Nutrient Deficiency</h4>
                    <p>Lack of essential nutrients can lead to stunted growth and discoloration.</p>
                </div>
                <div class="plant-card">
                    <h4>🧪 Chemical Damage</h4>
                    <p>Overuse or misuse of fertilizers, pesticides, or herbicides can cause leaf burn, discoloration, or stunted growth. Always follow recommended guidelines for chemical applications.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

