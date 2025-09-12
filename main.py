"""
Koteria - HTML File Processing Application

Main entry point for the Koteria application with simplified structure.
"""

import streamlit as st
from streamlit_option_menu import option_menu
from app.config import get_credentials
from app.utils import initialize_session_state
from app.pages.dashboard import welcome
from app.pages.file_converter import convert_file

def show_login_page():
    """Display the login page."""
    st.title("Koteria Login")
    st.markdown("---")
    
    with st.form("login_form"):
        st.subheader("Enter your credentials")
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        submit_button = st.form_submit_button("Login", use_container_width=True)
        
        if submit_button:
            credentials = get_credentials()
            if username in credentials and credentials[username] == password:
                st.session_state.authenticated = True
                st.session_state.current_user = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

def show_sidebar_navigation():
    """Display professional sidebar navigation using streamlit-option-menu."""
    
    # Custom CSS for clean white sidebar
    st.markdown("""
    <style>
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff !important;
        border-right: 1px solid #e0e0e0 !important;
    }
    
    /* Sidebar content */
    .css-1lcbmhc {
        background-color: #ffffff !important;
    }
    
    /* Remove container styling from option menu */
    .stOptionMenu > div > div {
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Logo section - 60% of previous size
        # st.image('assets/images/koteria_logo3.png', width=150)
    
        
        # Main navigation using option_menu with logout included
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard", "Analytics", "Notifications", "Appearance", 
                "Database", "Connections", "Timezones", "Documentation",
                "Authentication", "User management", "Security", "Payments",
                "Import data", "Export data", "Logout"
            ],
            icons=[
                "house", "graph-up", "bell", "palette",
                "database", "link-45deg", "clock", "book",
                "shield-lock", "people", "shield-check", "credit-card",
                "download", "upload", "box-arrow-right"
            ],
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                    "border-radius": "0",
                    "margin": "0",
                    "border": "none"
                },
                "icon": {
                    "color": "#2c3e50",
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "2px 0",
                    "padding": "12px 16px",
                    "color": "#2c3e50",
                    "background-color": "transparent",
                    "border-radius": "6px",
                    "transition": "all 0.2s ease"
                },
                "nav-link:hover": {
                    "background-color": "#f8f9fa",
                    "color": "#2c3e50",
                    "transform": "translateX(4px)"
                },
                "nav-link-selected": {
                    "background-color": "#007bff",
                    "color": "#ffffff"
                }
            }
        )
        
        # Handle navigation selection
        if selected:
            if selected == "Logout":
                # Handle logout
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            else:
                st.session_state.koteria_current_page = selected

def show_koteria_app():
    """Display the main Koteria application."""
    # Initialize session state
    initialize_session_state()
    
    # Show sidebar navigation with logo
    show_sidebar_navigation()
    
    # Get current page
    current_page = st.session_state.get('koteria_current_page', 'Dashboard')
    
    # Display the selected page
    if current_page == "Dashboard":
        welcome()
    elif current_page in ["Import data", "Export data"]:
        # These pages show the file converter
        convert_file()
    elif current_page in ["Analytics", "Notifications", "Appearance", "Database", "Connections", "Timezones", "Documentation", "Authentication", "User management", "Security", "Payments"]:
        # These pages show the dashboard for now
        welcome()
    else:
        st.error(f"Unknown page: {current_page}")

def main():
    """Main function to run the application."""
    # Configure page
    st.set_page_config(
        page_title="Koteria",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Logo will be added only after login
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        # User is authenticated, show the app
        show_koteria_app()
    else:
        # User is not authenticated, show login page
        show_login_page()

if __name__ == "__main__":
    main()