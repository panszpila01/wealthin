"""
Welcome Page - Koteria App

Welcome page with application overview and navigation.
"""

import streamlit as st
from app.config import get_app_config

def welcome():

    # Define the CSS style to hide the deploy button
    hide_deploy_button_style = """
    <style>
    .stDeployButton {
        visibility: hidden;
    }
    </style>
    """

    # Apply the style using st.markdown
    st.markdown(hide_deploy_button_style, unsafe_allow_html=True)

    """Display the welcome page with application overview."""
    config = get_app_config("koteria")
    st.markdown(f"<h1 style='font-size: 1.8rem; margin-bottom: 0.5em;'>Dashboard</h1>", unsafe_allow_html=True)
    
    # Revenue, Cost, and Savings cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="
            background-color: white;
            border: 2px solid #000000;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 4px;">Revenue</div>
            <div style="font-size: 28px; font-weight: bold; color: #27ae60;">$45,230</div>
            <div style="font-size: 12px; color: #7f8c8d; margin-top: 4px;">+12.5% from last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="
            background-color: white;
            border: 2px solid #000000;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 4px;">Cost</div>
            <div style="font-size: 28px; font-weight: bold; color: #e74c3c;">$28,450</div>
            <div style="font-size: 12px; color: #7f8c8d; margin-top: 4px;">+3.2% from last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="
            background-color: white;
            border: 2px solid #000000;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 4px;">Savings</div>
            <div style="font-size: 28px; font-weight: bold; color: #3498db;">$16,780</div>
            <div style="font-size: 12px; color: #7f8c8d; margin-top: 4px;">+25.8% from last month</div>
        </div>
        """, unsafe_allow_html=True)



    # Quick actions
    st.markdown("---")
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Go to File Converter", use_container_width=True):
            st.session_state.koteria_current_page = "File Converter"
            st.rerun()
    
    with col2:
        if st.session_state.get('current_dataframe') is not None:
            if st.button("View Data", use_container_width=True):
                st.session_state.koteria_current_page = "File Converter"
                st.rerun()
        else:
            st.button("View Data", disabled=True, use_container_width=True)
    
    with col3:
        if st.button("Refresh Page", use_container_width=True):
            st.rerun()
