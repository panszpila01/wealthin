"""
finance

Main entry point for the finance application with simplified structure.
"""

import streamlit as st
from streamlit_option_menu import option_menu
from app.config import get_credentials
from app.utils import initialize_session_state
from app.pages.dashboard import welcome
from app.pages.file_converter import convert_file
from app.pages.database import database

def show_login_page():
    """Display the login page."""
    st.title("Application Login")
    st.markdown("")
    
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
    
    /* Add vertical light grey line between sidebar and main content */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e0e0e0 !important;
    }
    
    /* Alternative selectors for sidebar border */
    .css-1d391kg {
        border-right: 1px solid #e0e0e0 !important;
    }
    
    .css-1cypcdb {
        border-right: 1px solid #e0e0e0 !important;
    }
    
    /* Remove top spacing from sidebar content - multiple selectors */
    .css-1lcbmhc {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove top spacing from sidebar container */
    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Remove top spacing from first element in sidebar */
    .css-1lcbmhc > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Force logo to top with larger negative margin */
    .css-1lcbmhc img {
        margin-top: -2rem !important;
        padding-top: 0 !important;
    }
    
    /* Alternative selectors for sidebar content */
    .css-1d391kg {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    .css-1cypcdb {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the sidebar block container */
    .stSidebar > div > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force first image in sidebar to top with larger negative margin */
    .stSidebar img {
        margin-top: -2rem !important;
        display: block !important;
    }
    
    /* Additional aggressive selectors */
    section[data-testid="stSidebar"] img {
        margin-top: -2rem !important;
        position: relative !important;
        top: -2rem !important;
    }
    
    /* Target any image in sidebar with multiple selectors */
    .css-1lcbmhc > div:first-child img,
    .css-1d391kg > div:first-child img,
    .css-1cypcdb > div:first-child img {
        margin-top: -2rem !important;
        padding-top: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        # Logo section - 60% of previous size
        st.image('assets/images/logo.png', width=180)
        
        # Main navigation using option_menu with logout included
        selected = option_menu(
            menu_title=None,
            options=[
                "Dashboard", "Convert data", "Database", "Logout"
            ],
            icons=[
                "house", "download", "database", "box-arrow-right"
            ],
            # options=[
            #     "Dashboard", "Convert data", "Logout"
            # ],
            # icons=[
            #     "house", "download", "box-arrow-right"
            # ],
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
                    "background-color": "#f8f9fa",
                    "color": "#2c3e50"
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
                st.session_state.finance_current_page = selected

def show_wealthin_app():
    """Display the main finance application."""
    # Initialize session state
    initialize_session_state()
    
    # Show sidebar navigation with logo
    show_sidebar_navigation()
    
    # Get current page
    current_page = st.session_state.get('finance_current_page', 'Dashboard')
    
    # Display the selected page
    if current_page == "Dashboard":
        welcome()
    elif current_page in ["Convert data"]:
        # These pages show the file converter
        convert_file()
    elif current_page == "Database":
        # Show the database page with Airtable integration
        database()
    else:
        st.error(f"Unknown page: {current_page}")

def main():
    """Main function to run the application."""
    # Configure page
    st.set_page_config(
        page_title="Finance",
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
        show_wealthin_app()
    else:
        # User is not authenticated, show login page
        show_login_page()

if __name__ == "__main__":
    main()