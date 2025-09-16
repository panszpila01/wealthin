"""
Database Page - Airtable Integration

Display Airtable records in a Streamlit dataframe.
"""

import streamlit as st
import pandas as pd
import json
from app.utils.airtable import AirtableManager
from typing import List, Dict, Any
from io import BytesIO

def upload_csv_to_airtable(csv_file, table_name):
    """
    Upload CSV data to Airtable.
    
    Args:
        csv_file: Uploaded CSV file
        table_name: Name of the Airtable table
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Initialize Airtable manager
        airtable_manager = AirtableManager()
        
        if not airtable_manager.is_configured():
            st.error("Airtable is not properly configured. Please check your secrets.toml file.")
            return False
        
        # Convert DataFrame to list of records
        records = []
        for _, row in df.iterrows():
            # Convert row to dictionary, handling NaN values and data types
            record = {}
            for col, value in row.items():
                if pd.notna(value):  # Only include non-null values
                    # Handle different data types
                    if isinstance(value, str):
                        # Check if it's a JSON string that should be parsed
                        if value.strip().startswith('[') and value.strip().endswith(']'):
                            try:
                                record[col] = json.loads(value)
                            except:
                                record[col] = value
                        else:
                            record[col] = value
                    elif isinstance(value, (int, float)):
                        record[col] = value
                    elif hasattr(value, 'isoformat'):  # datetime objects
                        record[col] = value.isoformat()
                    else:
                        record[col] = str(value)
            records.append(record)
        
        # Upload records in batches (Airtable has a limit of 10 records per request)
        batch_size = 10
        total_uploaded = 0
        
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            
            # Upload batch
            for i, record in enumerate(batch):
                try:
                    success = airtable_manager.add_record(table_name, record)
                    if success:
                        total_uploaded += 1
                    else:
                        st.error(f"Failed to upload record {i+1}: {record}")
                        return False
                except Exception as e:
                    st.error(f"Error uploading record {i+1}: {str(e)}")
                    st.error(f"Problematic record data: {record}")
                    return False
        
        st.success(f"Successfully uploaded {total_uploaded} records to '{table_name}' table!")
        return True
        
    except Exception as e:
        st.error(f"Error uploading to Airtable: {str(e)}")
        return False

def show_database_page():
    """Display the database page with Airtable integration."""
    
    st.title("Database - Airtable Integration")
    st.markdown("View and manage data from your Airtable base.")
    
    # Initialize Airtable manager
    airtable_manager = AirtableManager()
    
    if not airtable_manager.is_configured():
        st.error("❌ Airtable is not properly configured. Please check your secrets.toml file.")
        return

    
    # Table selection
    st.markdown("---")
    st.subheader("Table Selection")
    
    available_tables = airtable_manager.get_table_names()
    
    # Create display options with user-friendly names
    table_options = {}
    for table_id in available_tables:
        display_name = airtable_manager.get_table_display_name(table_id)
        table_options[display_name] = table_id
    
    selected_display_name = st.selectbox(
        "Select a table to view:",
        options=list(table_options.keys()),
        help="Choose which Airtable table you want to view and download."
    )
    selected_table = table_options[selected_display_name]
    
    # Fetch data buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Load Table Data", help="Clear cache and load fresh data"):
            airtable_manager.clear_cache()
            with st.spinner(f"Refreshing data from '{selected_table}' table..."):
                df = airtable_manager.get_table_data_fresh(selected_table)
                if not df.empty:
                    st.session_state.airtable_data = df
                    st.session_state.airtable_filename = f"{selected_table}_data"
                    st.session_state.selected_table = selected_table
                    st.success(f"Successfully refreshed {len(df)} records from '{selected_table}'!")
                else:
                    st.warning(f"No data found in the '{selected_table}' table.")
    
    with col2:
        if st.button("Clear All Cache", help="Clear all Streamlit caches to fix API issues"):
            airtable_manager.clear_all_cache()
            st.success("All caches cleared! Try loading data again.")
    
    # Display data if available
    if 'airtable_data' in st.session_state and not st.session_state.airtable_data.empty:
        st.markdown("---")
        table_name = st.session_state.get('selected_table', 'Unknown')
        df = st.session_state.airtable_data
        
        # # Display options
        # st.markdown("#### Display Options")
        # col1, col2 = st.columns(2)
        
        # with col1:
        #     show_columns = st.multiselect(
        #         "Select columns to display:",
        #         options=df.columns.tolist(),
        #         default=df.columns.tolist()[:5]  # Show first 5 columns by default
        #     )
        
        # with col2:
        #     max_rows = st.slider("Maximum rows to display:", 10, len(df), min(100, len(df)))
        
        # # Filter data based on selection
        # if show_columns:
        #     display_df = df[show_columns].head(max_rows)
        # else:
        #     display_df = df.head(max_rows)
        
        # Display the dataframe
        st.markdown(f"Data Preview - {table_name}")
        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )
        
        # Data info
        with st.expander("Data Information"):
            st.markdown("**Column Information:**")
            for col in df.columns:
                st.write(f"- **{col}**: {df[col].dtype} ({df[col].notna().sum()} non-null values)")
        
        # Download options
        st.markdown("#### Download Data")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv_data,
                file_name=f"{st.session_state.airtable_filename}.csv",
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
                file_name=f"{st.session_state.airtable_filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        with col3:
            if st.button("Clear Data"):
                if 'airtable_data' in st.session_state:
                    del st.session_state.airtable_data
                if 'airtable_filename' in st.session_state:
                    del st.session_state.airtable_filename
                st.rerun()
    
    # CSV to Airtable Upload Section
    st.markdown("---")
    st.markdown("### Upload CSV to Airtable")
    
    # Initialize Airtable manager for table selection
    airtable_manager = AirtableManager()
    
    if airtable_manager.is_configured():
        # Get available tables
        available_tables = airtable_manager.get_table_names()
        
        # Create display options with user-friendly names
        table_options = {}
        for table_id in available_tables:
            display_name = airtable_manager.get_table_display_name(table_id)
            table_options[display_name] = table_id
        
        # CSV file upload
        csv_file = st.file_uploader(
            "Upload CSV file to import to Airtable",
            type=['csv'],
            help="Select a CSV file to upload to Airtable",
            key="csv_uploader"
        )
        
        # Table selection
        selected_display_name = st.selectbox(
            "Select Airtable table:",
            options=list(table_options.keys()),
            help="Choose which Airtable table to upload the data to"
        )
        selected_table = table_options[selected_display_name]
        
        # Upload button
        if csv_file is not None and selected_table:
            if st.button("Upload to Airtable", type="primary"):
                with st.spinner(f"Uploading {csv_file.name} to '{selected_table}' table..."):
                    success = upload_csv_to_airtable(csv_file, selected_table)
                    if success:
                        st.balloons()  # Celebration animation
    else:
        st.error("Airtable is not properly configured. Please check your secrets.toml file.")

def database():
    """Main function for the database page."""
    show_database_page()
