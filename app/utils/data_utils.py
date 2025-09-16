"""
Data Utilities for App

Common data processing utilities and sample data functions.
"""

import streamlit as st
import pandas as pd


class DataUtils:
    """Utility class for data operations."""
    
    @staticmethod
    @st.cache_data
    def get_sample_data() -> pd.DataFrame:
        """Get sample data for demonstration purposes."""
        return pd.DataFrame({
            'animal_name': ['Rex', 'Bella', 'Max'],
            'owner': ['John Doe', 'Jane Smith', 'Bob Johnson'],
            'visit_date': ['2024-01-15', '2024-01-16', '2024-01-17'],
            'treatment': ['Vaccination', 'Checkup', 'Surgery']
        })


# Convenience functions for backward compatibility
@st.cache_data
def get_sample_data() -> pd.DataFrame:
    """Get sample data for demonstration purposes."""
    return DataUtils.get_sample_data()
