import streamlit as st
import db_functions
import auth_functions
import time

# Page config
st.set_page_config(
    page_title="AgriAssist - Sign In",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file {file_name} not found. Using default styling.")

# Load CSS with error handling
load_css("style_pro.css")

# Initialize database
try:
    db_functions.setup_database()
except Exception as e:
    st.error(f"Database initialization failed: {e}")
    st.stop()

# Check if already logged in
if 'logged_in' in st.session_state and st.session_state.logged_in:
    if st.session_state.get('role') == 'Admin':
        st.switch_page("pages/7_Admin_Dashboard.py")
    else:
        st.switch_page("pages/1_Dashboard.py")

# Main container
st.markdown("""
<div class="login-container">
    <div class="login-card">
        <div class="login-logo">
            <h1>AgriAssist</h1>
        </div>
        <p class="login-tagline">Connect with farmers and grow together</p>
""", unsafe_allow_html=True)

# Login Form
tab1, tab2 = st.tabs(["Sign In", "Create Account"])

with tab1:
    with st.form("login_form"):
        username = st.text_input("Email or Phone", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        login_btn = st.form_submit_button("Log In")
        
        if login_btn:
            if not username or not password:
                st.error("Please enter both username and password")
            
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                with st.spinner("Signing in..."):
                    try:
                        user = db_functions.get_user(username)
                        if user and auth_functions.verify_password(password, user['password_hash']):
                            st.session_state['logged_in'] = True
                            st.session_state['username'] = user['username']
                            st.session_state['role'] = user['role']
                            
                            # Show success and redirect
                            success = st.success("Login successful! Redirecting...")
                            time.sleep(1)
                            
                            if user['role'] == 'Admin':
                                st.switch_page("pages/7_Admin_Dashboard.py")
                            else:
                                st.switch_page("pages/1_Dashboard.py")
                            st.rerun()
                        else:
                            st.error("Incorrect username or password.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    # Forgot password link
    st.markdown("<a href='#forgot-password' class='forgot-password'>Forgot Password?</a>", unsafe_allow_html=True)
    
    # Divider
    st.markdown("<div class='divider'>or</div>", unsafe_allow_html=True)
    
    # Social login buttons
    st.button("Continue with Google", use_container_width=True)
    st.button("Continue with Facebook", use_container_width=True)

with tab2:
    with st.form("signup_form"):
        fullname = st.text_input("Full Name", key="signup_fullname")
        email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("New Password", type="password", key="signup_new_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        signup_btn = st.form_submit_button("Sign Up")
        
        if signup_btn:
            username = email
            password = new_password
            
            if not all([username, password, confirm_password]):
                st.error("All fields are required")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long.")
            elif db_functions.get_user(username):
                st.error("An account with this email already exists.")
            else:
                try:
                    hashed_password = auth_functions.hash_password(password)
                    db_functions.add_user(username, hashed_password, "Client")
                    st.success("Account created successfully! Please sign in.")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating account: {str(e)}")

# Close the container
st.markdown("""
    </div>
    <div class="signup-link">
        By proceeding, you agree to our <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
    </div>
</div>
""", unsafe_allow_html=True)

