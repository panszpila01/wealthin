"""
Configuration system for Koteria App.

Centralized configuration management following Streamlit best practices.
"""
import streamlit as st
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class AppConfig:
    """Configuration for individual apps."""
    name: str
    display_name: str
    layout: str = "wide"  # "wide" or "narrow"
    page_icon: str = "📊"
    custom_settings: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.custom_settings is None:
            self.custom_settings = {}


# App configurations
APP_CONFIGS = {
    "finance": AppConfig(
        name="finance",
        display_name="finance",
        layout="wide",
        page_icon="",
        custom_settings={
            "supported_file_types": ["html"],
            "show_dataframe_info": True
        }
    )
}

# User to app mapping
USER_APP_MAPPING = {
    "Wealthin": "finance"
}

def get_app_config(app_name: str) -> AppConfig:
    """Get configuration for an app."""
    return APP_CONFIGS.get(app_name)


def get_user_app(username: str) -> str:
    """Get the app name for a user."""
    return USER_APP_MAPPING.get(username, "koteria")  # default to koteria


def get_credentials() -> Dict[str, str]:
    """Get all credentials from secrets.toml or fallback to defaults."""
    try:
        # Try to get credentials from secrets.toml
        if "login" in st.secrets and "credentials" in st.secrets["login"]:
            return st.secrets["login"]["credentials"]
    except Exception as e:
        st.error(f"Error getting credentials: {e}")
