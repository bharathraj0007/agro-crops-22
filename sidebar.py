import streamlit as st
from translations import get_text

def authenticated_sidebar():
    """Creates a sidebar for authenticated users."""
    with st.sidebar:
        st.markdown("🌱 **AgriAssist**")
        # from translations import get_language_switcher # Local import to avoid circular dependency
        # get_language_switcher()

        st.page_link("pages/1_Dashboard.py", label=get_text("home"), icon="🏠")
        st.page_link("pages/2_Recommendations.py", label=get_text("recommendations"), icon="✅")
        st.page_link("pages/3_Insights.py", label=get_text("insights"), icon="📊")
        st.page_link("pages/4_History.py", label=get_text("history"), icon="📜")
        st.page_link("pages/5_Support.py", label=get_text("support"), icon="💬")
        st.page_link("pages/6_Profile.py", label=get_text("profile"), icon="👤")
        st.page_link("pages/10_Marketing.py", label=get_text("marketing"), icon="📈")
        st.page_link("pages/11_Govt_Schemes.py", label=get_text("government_schemes"), icon="🏦")
        st.page_link("pages/0_Dr.Plant.py", label=get_text("Dr.plant"), icon="🌱")

        st.markdown("---")

        if st.button(get_text("logout"), use_container_width=True, key="sidebar_logout"):
            for key in list(st.session_state.keys()):
                if key in ['logged_in', 'username', 'role', 'lang']:
                    del st.session_state[key]
            st.rerun()