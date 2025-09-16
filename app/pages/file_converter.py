"""
File Converter Page - App

Handles file upload and processing functionality.
Following Streamlit best practices for multipage applications.
"""

import streamlit as st
import tempfile
import pandas as pd
import os
import hashlib
from io import BytesIO
from app.config import get_app_config
from app.utils.html_processor import read_html

@st.cache_data
def process_html_file(file_content: bytes, filename: str):
    """
    Cached function to process HTML files.
    This prevents re-processing the same file multiple times.
    """
    try:
        # Save uploaded file temporarily to read it
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.html') as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        try:
            df = read_html(tmp_file_path, filename)
            return df
        finally:
            # Clean up temporary file
            os.unlink(tmp_file_path)
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


def convert_file():
    """Display the file upload page with improved session state management."""
    config = get_app_config("finance")
    
    st.markdown("### File Upload & Processing")
    
    # File upload
    supported_types = config.custom_settings.get("supported_file_types", ["html"])
    uploaded_file = st.file_uploader(
        "Drag and drop a file here", 
        type=supported_types,
        help=f"Supported formats: {', '.join(supported_types)}",
        key="file_uploader"
    )
    
    # Clear data button (show when data is loaded)
    if st.session_state.get('current_dataframe') is not None:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"Currently loaded: {st.session_state.get('current_filename', 'Unknown')}")
        with col2:
            if st.button("Clear Data", help="Clear the loaded data and cache"):
                # Clear session state
                st.session_state.current_dataframe = None
                st.session_state.current_filename = None
                st.session_state.file_processed = False
                # Clear the cache for the processing function
                process_html_file.clear()
                st.rerun()
    
    # Process file if uploaded
    if uploaded_file is not None:
        # Always process the file (this will use cache if same file, but allows reprocessing)
        with st.spinner("Processing file..."):
            if uploaded_file.name.endswith('.html'):
                # Create a unique cache key that includes file content hash to ensure fresh processing
                file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()
                cache_key = f"{uploaded_file.name}_{file_hash}"
                
                df = process_html_file(uploaded_file.getvalue(), cache_key)
            else:
                st.error("Unsupported file type!")
                df = None
            
            if df is not None:
                # Store in session state for other pages
                st.session_state.current_dataframe = df
                st.session_state.current_filename = uploaded_file.name
                st.session_state.file_processed = True
            else:
                st.session_state.file_processed = False
    
    # Display data if available
    if st.session_state.current_dataframe is not None:
        df = st.session_state.current_dataframe
        
        st.markdown("### Processed Data")
        
        # Display the dataframe
        st.dataframe(df, use_container_width=True, height=400)
        
        # Download options
        st.markdown("#### Download Data")
        col1, col2 = st.columns(2)
        
        with col1:
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv_data,
                file_name=f"processed_{st.session_state.current_filename}.csv",
                mime="text/csv"
            )
        
        with col2:
            # Create Excel data in memory
            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_data = excel_buffer.getvalue()
            st.download_button(
                label="Download as Excel",
                data=excel_data,
                file_name=f"processed_{st.session_state.current_filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.info("Please upload an HTML file to get started")
