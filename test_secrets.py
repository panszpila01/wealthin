#!/usr/bin/env python3
"""
Test script to verify secrets loading
"""
import streamlit as st
import sys
import os
sys.path.append('.')

def test_secrets():
    """Test if secrets are loaded correctly."""
    print("=== Testing Secrets Loading ===")
    
    try:
        # Check if st.secrets is available
        print(f"st.secrets available: {hasattr(st, 'secrets')}")
        
        if hasattr(st, 'secrets'):
            print(f"st.secrets type: {type(st.secrets)}")
            print(f"st.secrets content: {st.secrets}")
            
            # Check login section
            if "login" in st.secrets:
                print(f"Login section found: {st.secrets['login']}")
                if "credentials" in st.secrets["login"]:
                    print(f"Credentials found: {st.secrets['login']['credentials']}")
                else:
                    print("Credentials not found in login section")
            else:
                print("Login section not found in secrets")
        else:
            print("st.secrets is not available")
            
    except Exception as e:
        print(f"Error testing secrets: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_secrets()
