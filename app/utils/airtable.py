"""
Airtable Manager - Handle all Airtable operations.

This module provides a class to manage Airtable operations including
reading, adding, updating, and deleting records.
"""

import streamlit as st
import pandas as pd
from pyairtable import Api
from typing import List, Dict, Any, Optional
import os


class AirtableManager:
    """Manager class for Airtable operations."""
    
    def __init__(self, api_key: str = None, base_id: str = None):
        """
        Initialize Airtable manager.
        
        Args:
            api_key: Airtable API key. If None, will try to get from secrets.
            base_id: Airtable base ID. If None, will try to get from secrets.
        """
        self.api_key = api_key or self._get_api_key()
        self.base_id = base_id or self._get_base_id()
        self.api = None
        
        if self.api_key and self.base_id:
            self.api = Api(self.api_key)
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from Streamlit secrets."""
        try:
            return st.secrets.get("airtable", {}).get("api_key")
        except Exception:
            return None
    
    def _get_base_id(self) -> Optional[str]:
        """Get base ID from Streamlit secrets."""
        try:
            return st.secrets.get("airtable", {}).get("base_id")
        except Exception:
            return None
    
    @st.cache_data
    def get_table_data(_self, table_name: str, cache_key: str = None) -> pd.DataFrame:
        """
        Fetch all records from a specific table and return as DataFrame.
        
        Args:
            table_name: Name of the Airtable table
            cache_key: Optional cache key to force refresh (use timestamp)
            
        Returns:
            pandas DataFrame with table records
        """
        if not _self.api:
            return pd.DataFrame()
        
        # Retry logic for API calls
        max_retries = 3
        for attempt in range(max_retries):
            try:
                table = _self.api.table(_self.base_id, table_name)
                records = table.all()
                
                if records:
                    # Extract fields from records
                    data = []
                    for record in records:
                        row = record['fields'].copy()
                        row['id'] = record['id']  # Add record ID
                        data.append(row)
                    
                    return pd.DataFrame(data)
                else:
                    return pd.DataFrame()
                    
            except Exception as e:
                error_msg = str(e)
                if "403" in error_msg and attempt < max_retries - 1:
                    # Wait before retry for 403 errors
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    st.error(f"Error fetching data from Airtable table '{table_name}': {error_msg}")
                    if "403" in error_msg:
                        st.warning("💡 **Troubleshooting tip**: This might be a temporary API issue. Try refreshing the page or clearing the cache.")
                    return pd.DataFrame()
        
        return pd.DataFrame()
    
    def get_table_data_fresh(self, table_name: str) -> pd.DataFrame:
        """
        Fetch fresh data from Airtable table (bypasses cache).
        
        Args:
            table_name: Name of the Airtable table
            
        Returns:
            pandas DataFrame with table records
        """
        import time
        # Use timestamp as cache key to force fresh data
        cache_key = f"{table_name}_{int(time.time())}"
        return self.get_table_data(table_name, cache_key)
    
    def clear_cache(self):
        """Clear the cache for get_table_data."""
        self.get_table_data.clear()
    
    def clear_all_cache(self):
        """Clear all Streamlit caches."""
        st.cache_data.clear()
    
    def get_table_names(self) -> List[str]:
        """
        Get list of available table names from secrets or return default.
        
        Returns:
            List of table names/IDs
        """
        try:
            # Try to get from secrets first
            tables = st.secrets.get("airtable", {}).get("tables", [])
            if tables:
                return tables
            else:
                raise Exception("No tables found in secrets")
            
        except Exception as e:
            st.error(f"Error getting table names: {e}")
            return []
    
    def get_table_display_name(self, table_id: str) -> str:
        """
        Get a user-friendly display name for a table ID.
        
        Args:
            table_id: The table ID (e.g., tblLIYZQpcmJfadxa)
            
        Returns:
            User-friendly display name
        """
        # Map table IDs to display names
        table_names = {
            "tblLIYZQpcmJfadxa": "Transactions",
            "chart_of_account": "Chart of Accounts"
        }
        return table_names.get(table_id, table_id)
    
    def add_record(self, table_name: str, fields: Dict[str, Any]) -> bool:
        """
        Add a new record to the specified table.
        
        Args:
            table_name: Name of the Airtable table
            fields: Dictionary of field names and values
            
        Returns:
            True if successful, False otherwise
        """
        if not self.api:
            return False
        
        try:
            table = self.api.table(self.base_id, table_name)
            table.create(fields)
            return True
        except Exception as e:
            st.error(f"Error adding record to table '{table_name}': {str(e)}")
            return False
    
    def update_record(self, table_name: str, record_id: str, fields: Dict[str, Any]) -> bool:
        """
        Update an existing record in the specified table.
        
        Args:
            table_name: Name of the Airtable table
            record_id: ID of the record to update
            fields: Dictionary of field names and values to update
            
        Returns:
            True if successful, False otherwise
        """
        if not self.api:
            return False
        
        try:
            table = self.api.table(self.base_id, table_name)
            table.update(record_id, fields)
            return True
        except Exception as e:
            st.error(f"Error updating record in table '{table_name}': {str(e)}")
            return False
    
    def delete_record(self, table_name: str, record_id: str) -> bool:
        """
        Delete a record from the specified table.
        
        Args:
            table_name: Name of the Airtable table
            record_id: ID of the record to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.api:
            return False
        
        try:
            table = self.api.table(self.base_id, table_name)
            table.delete(record_id)
            return True
        except Exception as e:
            st.error(f"Error deleting record from table '{table_name}': {str(e)}")
            return False
    
    def is_configured(self) -> bool:
        """
        Check if Airtable is properly configured.
        
        Returns:
            True if API key and base ID are available
        """
        return bool(self.api_key and self.base_id and self.api)
