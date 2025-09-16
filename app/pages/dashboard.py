"""
Welcome Page - Koteria App

Welcome page with application overview and navigation.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from app.utils.airtable import AirtableManager
from app.config import get_app_config

def welcome():
    """Display the welcome page with application overview."""
    
    # CSS to move title to top - maximum positioning
    st.markdown("""
    <style>
    /* Move main content title to top - aggressive positioning */
    .main .block-container {
        padding-top: 0rem !important;
        margin-top: 0rem !important;
    }
    
    /* Target the first element (title) in main content */
    .main .block-container > div:first-child {
        margin-top: -4rem !important;
        padding-top: 0 !important;
    }
    
    /* Alternative selectors for main content */
    .css-1d391kg {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Force title to top - maximum negative margin */
    h1 {
        margin-top: -4rem !important;
        padding-top: 0 !important;
    }
    
    /* Target main content area - maximum positioning */
    .main .block-container h1 {
        margin-top: -4rem !important;
        position: relative !important;
        top: -4rem !important;
    }
    
    /* Additional aggressive selectors */
    .main h1 {
        margin-top: -4rem !important;
        position: relative !important;
        top: -4rem !important;
    }
    
    /* Target any h1 in main content */
    .main .block-container > div:first-child h1 {
        margin-top: -4rem !important;
        padding-top: 0 !important;
        position: relative !important;
        top: -4rem !important;
    }
    
    /* Force main content to start at very top */
    .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Target the main content area directly */
    .main .block-container > div:first-child {
        margin-top: -4rem !important;
        padding-top: 0 !important;
        position: relative !important;
        top: -4rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    config = get_app_config("finance")
    col1, col2 = st.columns(2)
    with col1:
        st.title("Dashboard")
        # Add horizontal line below title - full width
        st.markdown("""
        <div style="
            height: 1px;
            background-color: #e0e0e0;
            margin-top: 10px;
            margin-bottom: 20px;
            margin-left: -2rem;
            margin-right: -2rem;
            width: calc(100vw - 2rem);
            position: relative;
            left: 2rem;
        "></div>
        """, unsafe_allow_html=True)
    # with col2:
    #     if st.button("Refresh Page", use_container_width=True):
    #         st.rerun()
    
    st.markdown("")
    st.markdown("Overview")
    
    # Initialize Airtable manager
    airtable_manager = AirtableManager()
    
    if airtable_manager.is_configured():
        # Fetch and display wizyty table data
        with st.spinner("Loading data from Airtable..."):
            transactions_df = airtable_manager.get_table_data("transactions")
            chart_of_accounts_df = airtable_manager.get_table_data("chart_of_accounts")
            df = pd.merge(transactions_df, chart_of_accounts_df, on='account_id', how='left')
        
        if not df.empty:
            # Calculate counts for the cards
            try:
                assets_sum = sum(df[df['account_id'] == '1300']['amount']) if 'account_id' in df.columns and 'amount' in df.columns else 0
                liabilities_sum = sum(df[df['account_id'].isin(['2000','2100'])]['amount']) if 'account_id' in df.columns and 'amount' in df.columns else 0
                expenses_sum = sum(df[df['account_id'].isin(['4000','4100','4200','4300'])]['amount']) if 'account_id' in df.columns and 'amount' in df.columns else 0
                income_sum = sum(df[df['account_id'].isin(['5000','5100'])]['amount']) if 'account_id' in df.columns and 'amount' in df.columns else 0
                net_worth_sum = assets_sum + liabilities_sum
            except Exception as e:
                st.error(f"Error calculating financial summaries: {e}")
                assets_sum = liabilities_sum = expenses_sum = income_sum = 0
            
            # Display cards with actual counts
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 28px; font-weight: bold; color: #000000;">{assets_sum}</div>
                    <div style="font-size: 14px; font-weight: normal; color: #7f8c8d; margin-bottom: 4px;">Assets</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 28px; font-weight: bold; color: #000000;">{liabilities_sum}</div>
                    <div style="font-size: 14px; font-weight: normal; color: #7f8c8d; margin-bottom: 4px;">Liabilities</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="
                    background-color: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 20px;
                    text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 28px; font-weight: bold; color: #000000;">{net_worth_sum}</div>
                    <div style="font-size: 14px; font-weight: normal; color: #7f8c8d; margin-bottom: 4px;">Net Worth</div>
                </div>
                """, unsafe_allow_html=True)
            
            #Chart displaying expenses by category
            st.markdown("")
            st.markdown("Expenses by Category")
            
            # Filter for expense accounts and prepare chart data
            expenses_df = df[df['account_id'].isin(['4000','4100','4200','4300'])]
            if not expenses_df.empty:
                chart_df = expenses_df[['account_name', 'amount']].copy()
                # Make amounts positive for better chart display
                chart_df['amount'] = chart_df['amount'].abs()
                
                # Apply the container styling from the community code
                PLOT_BGCOLOR = "#ffffff"
                
                st.markdown(
                    f"""
                    <style>
                    .stPlotlyChart {{
                     outline: 1px solid #e0e0e0;
                     border-radius: 15px;
                     box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                     background-color: {PLOT_BGCOLOR};
                    }}
                    </style>
                    """, unsafe_allow_html=True
                )
                
                # Create Plotly bar chart with rounded bars
                fig = go.Figure(data=[
                    go.Bar(
                        x=chart_df['account_name'],
                        y=chart_df['amount'],
                        marker_color='#3498db',
                        text=chart_df['amount'],
                        textposition='none',
                        marker=dict(
                            line=dict(width=0),
                            cornerradius=15
                        )
                    )
                ])
                
                fig.update_layout(
                    title="",
                    xaxis_title="",
                    yaxis_title="",
                    paper_bgcolor=PLOT_BGCOLOR,
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(pad=0, r=0, t=2, b=20, l=20),
                    showlegend=False,
                    height=400
                )
                
                fig.update_xaxes(
                    showline=False, 
                    showgrid=False,
                    zeroline=False,
                    linewidth=0
                )
                fig.update_yaxes(
                    showline=False, 
                    showgrid=False,
                    zeroline=False,
                    linewidth=0
                )
                
                # Render the chart
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expense data available for chart.")

            # Latest Transactions Section
            st.markdown("")
            st.markdown("Last Transactions")
            
            # Display dataframe without index column and with padding, sorted by timestamp desc
            # Filter for expense accounts first, then select columns
            df = df[df['account_id'].isin(['3000','3100','4000','4100','4200','4300'])]
            df = df[['timestamp', 'counterparty', 'description', 'amount', 'currency']].head(10)
            # Convert timestamp to string format safely
            try:
                if 'timestamp' in df.columns:
                    # Convert to datetime first, then format
                    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce').dt.strftime('%Y-%m-%d')
                    # Fill any NaT values with empty string
                    df['timestamp'] = df['timestamp'].fillna('')
            except Exception as e:
                st.warning(f"Could not format timestamp column: {e}")
                # Keep original timestamp values if formatting fails
                pass
            
            df.rename(columns={'timestamp': 'Transaction Date', 'description': 'Description', 'amount': 'Amount', 'currency': 'Currency'}, inplace=True)
            
            # Sort by Transaction Date (which was originally timestamp)
            if 'Transaction Date' in df.columns:
                df_sorted = df.sort_values('Transaction Date', ascending=False)
            else:
                df_sorted = df
            
            # Create styled container for the table
            st.markdown("""
            <style>
            .stDataFrame {
                background-color: #ffffff;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                padding: 10px;
                margin-bottom: 20px;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                df_sorted, 
                use_container_width=True, 
                height=400, 
                hide_index=True
            )
        else:
            st.info("No data found in the 'transactions' table.")
    else:
        st.error("Airtable is not properly configured. Please check your secrets.toml file.")
