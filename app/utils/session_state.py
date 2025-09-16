"""
Session State Manager for Finance App

Manages all session state variables and provides utilities for state management.
"""

import streamlit as st
from typing import Dict, Any, Optional


class SessionStateManager:
    """Manager class for session state operations."""
    
    @staticmethod
    def initialize():
        """Initialize all session state variables for the app."""
        # Navigation state
        if 'finance_current_page' not in st.session_state:
            st.session_state.finance_current_page = "Dashboard"
        
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
    
    @staticmethod
    def clear_data():
        """Clear all data-related session state variables."""
        st.session_state.current_dataframe = None
        st.session_state.current_filename = None
        st.session_state.file_processed = False
    
    @staticmethod
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
    
    @staticmethod
    def display_data_info():
        """Display data information in a formatted way."""
        summary = SessionStateManager.get_data_summary()
        
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
    
    @staticmethod
    def show_sidebar_data_info():
        """Show data information in the sidebar."""
        summary = SessionStateManager.get_data_summary()
        
        if summary['loaded']:
            st.markdown("### 📊 Current Data")
            st.write(f"**File:** {summary['filename']}")
            st.write(f"**Shape:** {summary['shape'][0]} × {summary['shape'][1]}")
            st.write(f"**Memory:** {summary['memory_usage']:.1f} KB")
            
            if st.button("🗑️ Clear Data"):
                SessionStateManager.clear_data()
                st.rerun()
        else:
            st.markdown("### 📊 Current Data")
            st.info("No data loaded")


# Convenience functions for backward compatibility
def initialize_session_state():
    """Initialize all session state variables for the Finance app."""
    SessionStateManager.initialize()

def clear_data():
    """Clear all data-related session state variables."""
    SessionStateManager.clear_data()

def get_data_summary() -> Dict[str, Any]:
    """Get a summary of the current data in session state."""
    return SessionStateManager.get_data_summary()

def display_data_info():
    """Display data information in a formatted way."""
    SessionStateManager.display_data_info()

def show_sidebar_data_info():
    """Show data information in the sidebar."""
    SessionStateManager.show_sidebar_data_info()
