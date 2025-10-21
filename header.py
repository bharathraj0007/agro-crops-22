# import streamlit as st

# def custom_header(active_page):
#     """
#     Creates a custom vertical sidebar for navigation with icons,
#     dynamically changing based on the user's role.
#     """
    
#     # Define the pages for each role
#     client_pages = {
#         "Dashboard": {"icon": "🏠", "script": "1_Dashboard"},
#         "Recommendations": {"icon": "✅", "script": "2_Recommendations"},
#         "Insights": {"icon": "📊", "script": "3_Insights"},
#         "History": {"icon": "📜", "script": "4_History"},
#         "Support": {"icon": "💬", "script": "5_Support"},
#         "Profile": {"icon": "👤", "script": "6_Profile"}
#     }
    
#     admin_pages = {
#         "Admin Dashboard": {"icon": "👑", "script": "7_Admin_Dashboard"},
#         "User Management": {"icon": "👥", "script": "8_Admin_User_Management"},
#         "Crop Management": {"icon": "🌿", "script": "9_Admin_Crop_Management"},
#     }
    
#     # Display the correct title and menu based on the user's role
#     if st.session_state.get("role") == "Admin":
#         st.sidebar.title("👑 Admin Panel")
#         pages_to_display = admin_pages
#     else:
#         st.sidebar.title("🌱 AgriAssist")
#         pages_to_display = client_pages

#     # Create a page link for each page in the current menu
#     for page_name, page_info in pages_to_display.items():
#         st.sidebar.page_link(
#             f"pages/{page_info['script']}.py",
#             label=page_name,
#             icon=page_info['icon'],
#             disabled=(active_page == page_name)
#         )
        
#     # Add a logout button at the bottom of the sidebar
#     st.sidebar.markdown("---")
#     if st.sidebar.button("Logout"):
#         # Clear all session state keys to log out
#         for key in list(st.session_state.keys()):
#             del st.session_state[key]
#         st.switch_page("app.py")

import streamlit as st

def custom_header(active_page):
    """
    Creates a custom header for the page.
    This function is called from every page to ensure consistent page headers.
    """
    
    # Create a page header with the active page title
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{active_page}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )