
# # # 🔹 LOGIN FORM
# # # =============================
# # with col1:
# #     #st.markdown('<div class="form-card">', unsafe_allow_html=True)
# #     st.subheader("🔑 Login")
# #     with st.form("login_form"):
# #         username = st.text_input("Username", key="login_username")
# #         password = st.text_input("Password", type="password", key="login_password")
# #         submitted = st.form_submit_button("Login")
# #         if submitted:
# #             user = db_functions.get_user(username)
# #             if user and auth_functions.verify_password(password, user['password_hash']):
# #                 st.session_state['logged_in'] = True
# #                 st.session_state['username'] = user['username']
# #                 st.session_state['role'] = user['role']
# #                 st.success("✅ Logged in successfully! Redirecting...")
# #                 if user['role'] == 'Admin':
# #                     st.switch_page("pages/7_Admin_Dashboard.py")
# #                 else:
# #                     st.switch_page("pages/1_Dashboard.py")
# #             else:
# #                 st.error("❌ Incorrect username or password.")
# #     st.markdown('</div>', unsafe_allow_html=True)

# # # =============================
# # # 🧑‍🌾 CLIENT SIGNUP FORM
# # # =============================
# # with col2:
# #     #st.markdown('<div class="form-card">', unsafe_allow_html=True)
# #     st.subheader("🧑‍🌾 Client Sign Up")
# #     with st.form("client_signup_form"):
# #         new_username = st.text_input("Username", key="client_username")
# #         new_password = st.text_input("Password", type="password", key="client_password")
# #         confirm_password = st.text_input("Confirm Password", type="password", key="client_confirm")
# #         signup_submitted = st.form_submit_button("Sign Up")
# #         if signup_submitted:
# #             if new_password != confirm_password:
# #                 st.error("❌ Passwords do not match.")
# #             elif len(new_password) < 6:
# #                 st.warning("Password must be at least 6 characters long.")
# #             elif db_functions.get_user(new_username):
# #                 st.error("⚠️ Username already exists.")
# #             else:
# #                 hashed_password = auth_functions.hash_password(new_password)
# #                 db_functions.add_user(new_username, hashed_password, "Client")
# #                 st.success("🎉 Client account created successfully! Please log in.")
# #     st.markdown('</div>', unsafe_allow_html=True)

# # # =============================
# # # 🛠️ ADMIN SIGNUP FORM
# # # =============================
# # with col3:
# #     #st.markdown('<div class="form-card">', unsafe_allow_html=True)
# #     st.subheader("🛠️ Admin Sign Up")
# #     st.sidebar.page_link("pages/1_Dashboard.py", label=get_text("home"), icon="🏠", disabled=True)
# #     st.sidebar.page_link("pages/2_Recommendations.py", label=get_text("recommendations"), icon="✅")
# #     st.sidebar.page_link("pages/3_Insights.py", label=get_text("insights"), icon="📊")
# #     st.sidebar.page_link("pages/4_History.py", label=get_text("history"), icon="📜")
# #     st.sidebar.page_link("pages/5_Support.py", label=get_text("support"), icon="💬")
# #     st.sidebar.page_link("pages/6_Profile.py", label=get_text("profile"), icon="👤")
# #     st.sidebar.page_link("pages/10_Marketing.py", label=get_text("marketing"), icon="📈")
# #     st.sidebar.page_link("pages/11_Govt_Schemes.py", label=get_text("government_schemes"), icon="🏦")
# #     with st.form("admin_signup_form"):
# #         admin_username = st.text_input("Username", key="admin_username")
# #         admin_password = st.text_input("Password", type="password", key="admin_password")
# #         admin_secret = st.text_input("Admin Secret Key", type="password", key="admin_secret")
# #         admin_signup_submitted = st.form_submit_button("Sign Up")
# #         if admin_signup_submitted:
# #             correct_secret = st.secrets.get("ADMIN_CREATION_SECRET", "DEFAULT_SECRET")
# #             if admin_secret != correct_secret:
# #                 st.error("❌ Incorrect Admin Secret Key.")
# #             elif len(admin_password) < 6:
# #                 st.error("Password must be at least 6 characters long.")
# #             elif db_functions.get_user(admin_username):
# #                 st.error("⚠️ Username already exists.")
# #             else:
# #                 hashed_password = auth_functions.hash_password(admin_password)
# #                 db_functions.add_user(admin_username, hashed_password, "Admin")
# #                 st.success("✅ Admin account created successfully! Please login.")
# #     st.markdown('</div>', unsafe_allow_html=True)

# # # --- Footer ---
# # st.markdown("""
# # <div class="footer">
# # 🌾 Built with ❤️ by <b>Bharath Raj</b> | BE CSE | RajaRajeswari College of Engineering
# # </div>
# # """, unsafe_allow_html=True)


# # import streamlit as st
# # import db_functions
# # import auth_functions
# # import os

# # # --- Page Config ---
# # st.set_page_config(
# #     page_title="AgriAssist | Login",
# #     layout="centered",
# #     page_icon="🌱",
# #     initial_sidebar_state="collapsed"
# # )

# # # --- Load Custom CSS ---
# # def load_css(file_name):
# #     css_path = os.path.join(os.path.dirname(__file__), file_name)
# #     with open(css_path) as f:
# #         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# # load_css("style_pro.css")

# # # --- Hero Section ---
# # st.markdown("""
# # <div class="hero-section" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1524594157367-4e0c40aa03a4?q=80&w=1880&auto=format&fit=crop'); background-size: cover;">
# #   <h1>🌾 Login to AgriAssist</h1>
# #   <p>Empowering farmers with AI — Smart crop insights for every season.</p>
# # </div>
# # """, unsafe_allow_html=True)
# # # st.markdown("""
# # # <div class="hero-section">
# # #   <h1>🌾 Login to AgriAssist</h1>
# # #   <p>Empowering farmers with AI — Smart crop insights for every season.</p>
# # # </div>
# # # """, unsafe_allow_html=True)

# # # --- Initialize Database ---
# # db_functions.setup_database()

# # # --- Single Column Layout ---
# # #st.markdown('<div class="form-card">', unsafe_allow_html=True)

# # # ----------------------------
# # # 🔹 LOGIN FORM
# # # ----------------------------
# # st.subheader("Login")
# # with st.form("login_form"):
# #     username = st.text_input("Enter your username")
# #     password = st.text_input("Enter your password", type="password")
# #     submitted = st.form_submit_button("Login")

# #     if submitted:
# #         user = db_functions.get_user(username)
# #         if user and auth_functions.verify_password(password, user['password_hash']):
# #             st.session_state['logged_in'] = True
# #             st.session_state['username'] = user['username']
# #             st.session_state['role'] = user['role']
# #             st.success("✅ Logged in successfully! Redirecting...")
# #             if user['role'] == 'Admin':
# #                 st.switch_page("pages/7_Admin_Dashboard.py")
# #             else:
# #                 st.switch_page("pages/1_Dashboard.py")
# #         else:
# #             st.error("❌ Incorrect username or password.")

# # st.markdown("---")

# # # ----------------------------
# # # 🧑‍🌾 CLIENT SIGNUP LINK
# # # ----------------------------
# # if st.checkbox("Don't have an account? Create Client Account"):
# #     st.subheader("🧑‍🌾 Client Sign Up")
# #     with st.form("client_signup_form"):
# #         new_username = st.text_input("Choose a username", key="client_signup_username")
# #         new_password = st.text_input("Choose a password", type="password", key="client_signup_password")
# #         confirm_password = st.text_input("Confirm password", type="password", key="client_signup_confirm")
# #         signup_submitted = st.form_submit_button("Sign Up as Client")
# #         if signup_submitted:
# #             if new_password != confirm_password:
# #                 st.error("❌ Passwords do not match.")
# #             elif len(new_password) < 6:
# #                 st.warning("Password must be at least 6 characters long.")
# #             elif db_functions.get_user(new_username):
# #                 st.error("⚠️ Username already exists.")
# #             else:
# #                 hashed_password = auth_functions.hash_password(new_password)
# #                 db_functions.add_user(new_username, hashed_password, "Client")
# #                 st.success("🎉 Client account created successfully! Please log in.")

# # st.markdown("---")

# # # --- Footer ---
# # st.markdown("""
# # <div class="footer">
# # 🌾 Built with ❤️ by <b>Bharath Raj</b> | BE CSE | RajaRajeswari College of Engineering
# # </div>
# # """, unsafe_allow_html=True)


# # ===== IMPORTS =====
# from translations import get_text, get_language_switcher
# import streamlit as st
# import sys
# import os
# import datetime
# import requests
# from typing import Optional, Dict, Any

# # Local imports
# import db_functions
# import auth_functions

# # Initialize session state for language
# if 'lang' not in st.session_state:
#     st.session_state.lang = 'en'  # Default language

# # --- Language Switcher ---
# get_language_switcher()

# # --- Page Config ---
# st.set_page_config(
#     page_title=get_text("app_name"),
#     layout="centered",
#     page_icon="🌱",
#     initial_sidebar_state="collapsed"
# )

# # --- Load Custom CSS ---
# def load_css(file_name):
#     css_path = os.path.join(os.path.dirname(__file__), file_name)
#     with open(css_path) as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# load_css("style_pro.css")

# # --- Hero Section ---
# st.markdown("""
# <div class="hero-section" style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1524594157367-4e0c40aa03a4?q=80&w=1880&auto=format&fit=crop'); background-size: cover;">
#   <h1>🌾 Login to AgriAssist</h1>
#   <p>Empowering farmers with AI — Smart crop insights for every season.</p>
# </div>
# """, unsafe_allow_html=True)

# # --- Initialize Database ---
# db_functions.setup_database()

# # --- Single Column Layout ---
# #st.markdown('<div class="form-card">', unsafe_allow_html=True)

# # ----------------------------
# # 🔹 LOGIN FORM
# # ----------------------------
# st.subheader(get_text("login"))
# with st.form("login_form"):
#     username = st.text_input(get_text("username"))
#     password = st.text_input(get_text("password"), type="password")
#     submitted = st.form_submit_button(get_text("login_button"))

#     if submitted:
#         user = db_functions.get_user(username)
#         if user and auth_functions.verify_password(password, user['password_hash']):
#             st.session_state['logged_in'] = True
#             st.session_state['username'] = user['username']
#             st.session_state['role'] = user['role']
#             st.success("✅ Logged in successfully! Redirecting...")
#             if user['role'] == 'Admin':
#                 st.switch_page("pages/7_Admin_Dashboard.py")
#             else:
#                 st.switch_page("pages/1_Dashboard.py")
#         else:
#             st.error("❌ Incorrect username or password.")

# st.markdown("---")

# # ----------------------------
# # 🧑‍🌾 CLIENT SIGNUP LINK
# # ----------------------------
# if st.checkbox(get_text("create_client_account")):
#     st.subheader("🧑‍🌾 Client Sign Up")
#     with st.form("client_signup_form"):
#         new_username = st.text_input(get_text("choose_username"), key="client_signup_username")
#         new_password = st.text_input(get_text("choose_password"), type="password", key="client_signup_password")
#         confirm_password = st.text_input(get_text("confirm_password"), type="password", key="client_signup_confirm")
#         signup_submitted = st.form_submit_button(get_text("sign_up_as_client"))

#         if signup_submitted:
#             if new_password != confirm_password:
#                 st.error("❌ Passwords do not match.")
#             elif len(new_password) < 6:
#                 st.warning("Password must be at least 6 characters long.")
#             elif db_functions.get_user(new_username):
#                 st.error("⚠️ Username already exists.")
#             else:
#                 hashed_password = auth_functions.hash_password(new_password)
#                 db_functions.add_user(new_username, hashed_password, "Client")
#                 st.success("🎉 Client account created successfully! Please log in.")

# st.markdown("---")

# # --- Footer ---
# st.markdown("""
# <div class="footer">
# 🌾 Built with ❤️ by <b>Bharath Raj</b> | BE CSE | RajaRajeswari College of Engineering
# </div>
# """, unsafe_allow_html=True)


# # ===== IMPORTS =====
# from translations import get_text, get_language_switcher
# import streamlit as st
# import sys
# import os
# import datetime
# import requests
# from typing import Optional, Dict, Any

# # Local imports
# import db_functions
# import auth_functions

# # Initialize session state for language
# if 'lang' not in st.session_state:
#     st.session_state.lang = 'en'  # Default language

# # ===== CONFIGURATION =====
# PAGE_CONFIG = {
#     "page_title": get_text("app_name"),
#     "layout": "centered",
#     "page_icon": "🌱",
#     "initial_sidebar_state": "collapsed"
# }

# # ===== HELPER FUNCTIONS =====
# def load_css(file_name: str) -> None:
#     """Load and inject CSS styles with UTF-8 encoding."""
#     import os
#     ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
#     css_path = os.path.join(ROOT_DIR, file_name)
#     try:
#         with open(css_path, 'r', encoding='utf-8') as f:
#             st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f"Error loading CSS: {str(e)}")


# # Initialize page config
# st.set_page_config(
#     page_title="AgriAssist Dashboard",
#     page_icon="🌱",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Load CSS
# load_css("style_pro.css")

# def show_hero() -> None:
#     """Display the hero section with title and subtitle."""
#     st.markdown("""
#     <div class="hero-section" style="background-image: url('https://images.unsplash.com/photo-1524594157367-4e0c40aa03a4?q=80&w=1880&auto=format&fit=crop');">
#         <h1>🌾 Login to AgriAssist</h1>
#         <p>Empowering farmers with AI — Smart crop insights for every season.</p>
#     </div>
#     """, unsafe_allow_html=True)

# def handle_login(username: str, password: str) -> Optional[Dict[str, Any]]:
#     """Handle user login logic."""
#     user = db_functions.get_user(username)
#     if user and auth_functions.verify_password(password, user['password_hash']):
#         st.session_state.update({
#             'logged_in': True,
#             'username': user['username'],
#             'role': user['role']
#         })
#         return user
#     return None

# def show_login_form() -> None:
#     """Render the login form."""
#     with st.form("login_form"):
#         st.subheader("Login")
#         username = st.text_input("Username", key="login_username")
#         password = st.text_input("Password", type="password", key="login_password")
        
#         if st.form_submit_button("Login", use_container_width=True):
#             if user := handle_login(username, password):
#                 st.success("✅ Login successful! Redirecting...")
#                 st.switch_page(f"pages/{'7_Admin_Dashboard' if user['role'] == 'Admin' else '1_Dashboard'}.py")
#             else:
#                 st.error("❌ Invalid username or password")

# def show_client_signup() -> None:
#     """Render the client signup form."""
#     with st.form("client_signup_form"):
#         st.subheader("🧑‍🌾 Client Sign Up")
#         username = st.text_input("Choose a username", key="signup_username")
#         password = st.text_input("Choose a password", type="password", key="signup_password")
#         confirm_password = st.text_input("Confirm password", type="password", key="signup_confirm")
        
#         if st.form_submit_button("Create Account", type="primary", use_container_width=True):
#             if password != confirm_password:
#                 st.error("❌ Passwords do not match")
#             elif len(password) < 6:
#                 st.error("❌ Password must be at least 6 characters")
#             elif db_functions.get_user(username):
#                 st.error("⚠️ Username already exists")
#             else:
#                 hashed_pw = auth_functions.hash_password(password)
#                 db_functions.add_user(username, hashed_pw, "Client")
#                 st.success("🎉 Account created! Please log in.")

# # ===== MAIN APP =====
# def main():
#     # Initialize page config
#     st.set_page_config(**PAGE_CONFIG)
    
#     # Load custom CSS
#     load_css("style_pro.css")
    
#     # Initialize database
#     db_functions.setup_database()
    
#     # Show hero section
#     show_hero()
    
#     # Create tabs for different sections
#     login_tab, signup_tab = st.tabs(["Login", "Create Account"])
    
#     with login_tab:
#         show_login_form()
    
#     with signup_tab:
#         show_client_signup()
    
#     # Footer
#     st.markdown("---")
#     st.markdown("""
#     <div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 2rem;">
#         🌾 Built with ❤️ by <b>Bharath Raj</b> | BE CSE | RajaRajeswari College of Engineering
#     </div>
#     """, unsafe_allow_html=True)
# -*- coding: utf-8 -*-
# import streamlit as st
# from typing import Optional, Dict, Any

# # Local imports
# import db_functions
# import auth_functions
# from translations import get_text, get_language_switcher

# # --- Page Config (must be the first Streamlit command) ---
# st.set_page_config(
#     page_title=get_text("app_name"),
#     page_icon="🌱",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # --- Language and Session State Initialization ---
# if 'lang' not in st.session_state:
#     st.session_state.lang = 'en'  # Default language

# # ===== HELPER FUNCTIONS =====
# def load_css(file_name: str) -> None:
#     """Load and inject CSS styles with UTF-8 encoding."""
#     import os
#     try:
#         with open(file_name, 'r', encoding='utf-8') as f:
#             st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
#     except Exception as e:
#         st.error(f"Error loading CSS: {str(e)}")

# def show_hero() -> None:
#     """Display the hero section with title and subtitle."""
#     st.markdown(f"""
#     <div class="hero-section" style="background-image: url('https://images.unsplash.com/photo-1524594157367-4e0c40aa03a4?q=80&w=1880&auto=format&fit=crop');">
#         <h1>🌾 {get_text('login_to_app')}</h1>
#         <p>{get_text('hero_subtitle')}</p>
#     </div>
#     """, unsafe_allow_html=True)

# def handle_login(username: str, password: str) -> Optional[Dict[str, Any]]:
#     """Handle user login logic."""
#     try:
#         user = db_functions.get_user(username)
#         if user and auth_functions.verify_password(password, user['password_hash']):
#             st.session_state.update({
#                 'logged_in': True,
#                 'username': user['username'],
#                 'role': user['role']
#             })
#             return user
#     except Exception as e:
#         st.error(f"Database error: {e}")
#     return None

# def show_login_form() -> None:
#     """Render the login form."""
#     with st.form("login_form"):
#         st.subheader(get_text("login"))
#         username = st.text_input(get_text("username"), key="login_username")
#         password = st.text_input(get_text("password"), type="password", key="login_password")

#         if st.form_submit_button(get_text("login_button"), use_container_width=True, type="primary"):
#             if user := handle_login(username, password):
#                 st.success(f"✅ {get_text('login_success')}")
#                 st.switch_page(f"pages/{'7_Admin_Dashboard' if user['role'] == 'Admin' else '1_Dashboard'}.py")
#             else:
#                 st.error(f"❌ {get_text('invalid_credentials')}")

# def show_signup_form() -> None:
#     """Render the client signup form."""
#     with st.form("client_signup_form"):
#         st.subheader(f"🧑‍🌾 {get_text('client_signup')}")
#         username = st.text_input(get_text("choose_username"), key="signup_username")
#         password = st.text_input(get_text("choose_password"), type="password", key="signup_password")
#         confirm_password = st.text_input(get_text("confirm_password"), type="password", key="signup_confirm")

#         if st.form_submit_button(get_text("create_account"), type="primary", use_container_width=True):
#             if password != confirm_password:
#                 st.error(f"❌ {get_text('password_mismatch')}")
#             elif len(password) < 6:
#                 st.error(f"❌ {get_text('password_length')}")
#             elif db_functions.get_user(username):
#                 st.error(f"⚠️ {get_text('username_exists')}")
#             else:
#                 hashed_pw = auth_functions.hash_password(password)
#                 db_functions.add_user(username, hashed_pw, "Client")
#                 st.success(f"🎉 {get_text('account_created')}")

# # ===== MAIN APP =====
# def main():
#     """Main function to run the Streamlit app."""
#     load_css("style_pro.css")
#     db_functions.setup_database()

#     # Place language switcher in the main body for the login page
#     get_language_switcher()

#     show_hero()

#     login_tab, signup_tab = st.tabs([f"🔑 {get_text('login')}", f"🧑‍🌾 {get_text('signup')}"])

#     with login_tab:
#         show_login_form()

#     with signup_tab:
#         show_signup_form()

#     st.markdown("---")
#     st.markdown(
#         f"""
#         <div class="footer">
#             <p>🌾 {get_text('built_with_love')} <b>Bharath Raj</b> | BE CSE | RajaRajeswari College of Engineering</p>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

# if __name__ == "__main__":
#     main()

import streamlit as st
import db_functions
import auth_functions
import time

# --- Page Config (must be the first Streamlit command) ---
st.set_page_config(
    page_title="AgriAssist - Login",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Load Custom CSS ---
def load_css(file_name: str) -> None:
    with open(file_name, 'r', encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css("style_pro.css")

# --- Initialize Database ---
db_functions.setup_database()

# --- Hide sidebar on login page ---
st.markdown("<style>[data-testid='stSidebar'] {display: none;}</style>", unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero-section">
    <h1>🌾 Welcome to AgriAssist</h1>
    <p>Empowering farmers with AI — Smart crop insights for every season.</p>
</div>
""", unsafe_allow_html=True)

# --- Login & Signup Forms ---
login_tab, signup_tab = st.tabs(["🔑 Login", "🧑‍🌾 Sign Up"])

with login_tab:
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login", use_container_width=True, type="primary"):
            user = db_functions.get_user(username)
            if user and auth_functions.verify_password(password, user['password_hash']):
                st.session_state.update({'logged_in': True, 'username': user['username'], 'role': user['role']})
                st.success("✅ Logged in successfully! Redirecting...")
                time.sleep(1)
                if user['role'] == 'Admin':
                    st.switch_page("pages/7_Admin_Dashboard.py")
                else:
                    st.switch_page("pages/1_Dashboard.py")
            else:
                st.error("❌ Incorrect username or password.")

with signup_tab:
    with st.form("client_signup_form"):
        username = st.text_input("Choose a Username", key="signup_username")
        password = st.text_input("Choose a Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        if st.form_submit_button("Create Account", type="primary", use_container_width=True):
            if password != confirm_password: st.error("❌ Passwords do not match.")
            elif len(password) < 6: st.error("❌ Password must be at least 6 characters long.")
            elif db_functions.get_user(username): st.error("⚠️ Username already exists.")
            else:
                hashed_pw = auth_functions.hash_password(password)
                db_functions.add_user(username, hashed_pw, "Client")
                st.success("🎉 Account created! Please go to the Login tab.")

# --- Footer ---
st.markdown("---")
st.markdown("""<div class="footer"><p>🌾 Built with ❤️ by Bharath Raj</p></div>""", unsafe_allow_html=True)

