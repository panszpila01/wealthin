"""
Utilities for Koteria App

Common utility functions for data processing and session state management.
Following Streamlit best practices for directory structure.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any

def initialize_session_state():
    """Initialize all session state variables for the Koteria app."""
    # Navigation state
    if 'koteria_current_page' not in st.session_state:
        st.session_state.koteria_current_page = "Welcome Page"
    
    # Data state
    if 'current_dataframe' not in st.session_state:
        st.session_state.current_dataframe = None
    if 'current_filename' not in st.session_state:
        st.session_state.current_filename = None
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False
    
    # UI state
    if 'show_data_info' not in st.session_state:
        st.session_state.show_data_info = True

def clear_data():
    """Clear all data-related session state variables."""
    st.session_state.current_dataframe = None
    st.session_state.current_filename = None
    st.session_state.file_processed = False

def get_data_summary() -> Dict[str, Any]:
    """Get a summary of the current data in session state."""
    if st.session_state.current_dataframe is not None:
        df = st.session_state.current_dataframe
        return {
            'loaded': True,
            'filename': st.session_state.get('current_filename', 'Unknown'),
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum() / 1024,  # KB
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'null_counts': df.isnull().sum().to_dict()
        }
    else:
        return {
            'loaded': False,
            'filename': None,
            'shape': (0, 0),
            'memory_usage': 0,
            'columns': [],
            'dtypes': {},
            'null_counts': {}
        }

def display_data_info():
    """Display data information in a formatted way."""
    summary = get_data_summary()
    
    if summary['loaded']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Rows", summary['shape'][0])
            st.metric("Columns", summary['shape'][1])
        
        with col2:
            st.metric("Memory Usage", f"{summary['memory_usage']:.1f} KB")
            st.metric("File", summary['filename'])
        
        # Column information
        with st.expander("📋 Column Details"):
            for col in summary['columns']:
                dtype = summary['dtypes'][col]
                null_count = summary['null_counts'][col]
                st.write(f"**{col}**: {dtype} ({null_count} nulls)")
    else:
        st.info("No data loaded")

@st.cache_data
def get_sample_data() -> pd.DataFrame:
    """Get sample data for demonstration purposes."""
    return pd.DataFrame({
        'animal_name': ['Rex', 'Bella', 'Max'],
        'owner': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'visit_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
        'treatment': ['Vaccination', 'Checkup', 'Surgery']
    })

def show_sidebar_data_info():
    """Show data information in the sidebar."""
    summary = get_data_summary()
    
    if summary['loaded']:
        st.markdown("### 📊 Current Data")
        st.write(f"**File:** {summary['filename']}")
        st.write(f"**Shape:** {summary['shape'][0]} × {summary['shape'][1]}")
        st.write(f"**Memory:** {summary['memory_usage']:.1f} KB")
        
        if st.button("🗑️ Clear Data"):
            clear_data()
            st.rerun()
    else:
        st.markdown("### 📊 Current Data")
        st.info("No data loaded")

def validate_file_type(filename: str, supported_types: list) -> bool:
    """Validate if the file type is supported."""
    if not filename:
        return False
    
    file_extension = filename.split('.')[-1].lower()
    return file_extension in [ext.lower() for ext in supported_types]

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"
