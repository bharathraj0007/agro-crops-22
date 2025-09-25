# ---- header.py ----
import streamlit as st

def custom_header(active_page):
    """Creates a custom vertical sidebar for navigation with icons."""
    
    st.sidebar.title("🌿 AgriAssist")
    
    # Page names and their corresponding icons and script files
    pages = {
        "Dashboard": {"icon": "🏠", "script": "app"},
        "Recommendations": {"icon": "✅", "script": "2_Recommendations"},
        "Insights": {"icon": "📊", "script": "3_Insights"},
        "History": {"icon": "📜", "script": "4_History"},
        "Support": {"icon": "💬", "script": "5_Support"}
    }
    
    for page_name, page_info in pages.items():
        st.sidebar.page_link(
            f"pages/{page_info['script']}.py" if page_info['script'] != "app" else f"{page_info['script']}.py",
            label=page_name,
            icon=page_info['icon'], # Use the specified icon
            disabled=(active_page == page_name)
        )