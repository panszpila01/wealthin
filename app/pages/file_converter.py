"""
File Converter Page - Koteria App

Handles file upload and processing functionality.
Following Streamlit best practices for multipage applications.
"""

import streamlit as st
import tempfile
import pandas as pd
import os
from app.config import get_app_config
from app.html_processor import read_html
from st_aggrid import AgGrid, GridOptionsBuilder

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
    config = get_app_config("koteria")
    
    st.markdown("### File Upload & Processing")
    st.markdown("Upload an HTML file to process and analyze its content.")
    
    # File upload
    supported_types = config.custom_settings.get("supported_file_types", ["html"])
    uploaded_file = st.file_uploader(
        "Drag and drop a file here", 
        type=supported_types,
        help=f"Supported formats: {', '.join(supported_types)}",
        key="file_uploader"
    )
    
    # Process file if uploaded
    if uploaded_file is not None:
        # Check if this is a new file (different from current)
        current_filename = st.session_state.get('current_filename')
        if current_filename != uploaded_file.name or not st.session_state.get('file_processed', False):
            with st.spinner("Processing file..."):
                if uploaded_file.name.endswith('.html'):
                    df = process_html_file(uploaded_file.getvalue(), uploaded_file.name)
                else:
                    st.error("Unsupported file type!")
                    df = None
                
                if df is not None:
                    # Store in session state for other pages
                    st.session_state.current_dataframe = df
                    st.session_state.current_filename = uploaded_file.name
                    st.session_state.file_processed = True
                    st.success(f"Successfully processed {uploaded_file.name}")
                else:
                    st.session_state.file_processed = False
        else:
            # File already processed, use cached data
            df = st.session_state.current_dataframe
            st.info(f"Using cached data for {uploaded_file.name}")
    
    # Display data if available
    if st.session_state.current_dataframe is not None:
        df = st.session_state.current_dataframe
        
        st.markdown("### Processed Data")
        
        # Configure AgGrid options
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children")
        gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
        gridOptions = gb.build()
        
        # Display AgGrid
        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=True,
            theme='streamlit',  # Use streamlit theme
            enable_enterprise_modules=True,
            height=400,
            width='100%'
        )
        
        # Show selected rows info
        if grid_response['selected_rows']:
            st.markdown("### Selected Rows")
            selected_df = pd.DataFrame(grid_response['selected_rows'])
            st.dataframe(selected_df, use_container_width=True)
        
        # Show additional information
        if config.custom_settings.get("show_dataframe_info", True):
            st.markdown("### Data Information")
            
            # Show column information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Column Information:**")
                for col in df.columns:
                    dtype = str(df[col].dtype)
                    null_count = df[col].isnull().sum()
                    st.write(f"• {col}: {dtype} ({null_count} nulls)")
            
            with col2:
                st.markdown("**Quick Actions:**")
                
                # Download all data
                if st.button("Download All Data", key="download_all_btn"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Download All CSV",
                        data=csv,
                        file_name=f"processed_{st.session_state.current_filename}.csv",
                        mime="text/csv",
                        key="download_all_csv"
                    )
                
                # Download selected data (if any rows are selected)
                if grid_response['selected_rows']:
                    if st.button("Download Selected Data", key="download_selected_btn"):
                        selected_csv = pd.DataFrame(grid_response['selected_rows']).to_csv(index=False)
                        st.download_button(
                            label="Download Selected CSV",
                            data=selected_csv,
                            file_name=f"selected_{st.session_state.current_filename}.csv",
                            mime="text/csv",
                            key="download_selected_csv"
                        )
    else:
        st.info("Please upload an HTML file to get started")
